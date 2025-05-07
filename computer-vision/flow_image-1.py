import cv2
import numpy as np
import argparse

''' Draws a line on an image with color corresponding to the direction of line
 image im: image to draw line on
 float x, y: starting point of line
 float dx, dy: vector corresponding to line angle and magnitude
'''
def draw_line(im, x, y, dx, dy):
  
  angle = np.arctan2(dy, dx)
  length = np.sqrt(dx*dx + dy*dy)
  hue = ((angle + np.pi) / (2 * np.pi)) * 180

  color = np.array([hue, 255, 255], dtype=np.uint8)
  color = cv2.cvtColor(color.reshape(1, 1, 3), cv2.COLOR_HSV2BGR)[0, 0]
  
  color = (int(color[0]), int(color[1]), int(color[2]))

  start_point = (int(x), int(y))
  end_point = (int(x + dx), int(y + dy))
  
  thickness = 1
  cv2.line(im, start_point, end_point, color, thickness)


''' Make an integral image or summed area table from an image
 image im: image to process
 returns: image I such that I[x,y] = sum{i<=x, j<=y}(im[i,j])
'''
def make_integral_image(im):
  h, w = im.shape[:2]
  integral = np.zeros((h+1, w+1), dtype=np.float32)
  im_float = im.astype(np.float32)
  for y in range (h):
    for x in range (w):
      integral[y+1,x+1] = im_float[y, x] + integral[y+1, x]
      
  for y in range(1, h+1):
     for x in range(1, w+1):
         integral[y, x] += integral[y-1, x]
  return integral

''' Apply a box filter to an image using an integral image for speed
 image im: image to smooth
 int s: window size for box filter
 returns: smoothed image
'''
def box_filter_image(im, s):
  integral = make_integral_image(im)
  h, w = im.shape[:2]
  output = np.zeros_like(im, dtype=np.float32)
  half_s = s // 2
  for y in range(h):
     for x in range(w):
         x1 = max(0, x - half_s)
         y1 = max(0, y - half_s)
         x2 = min(w-1, x + half_s)
         y2 = min(h-1, y + half_s)
         sum_window = integral[y2+1, x2+1] - integral[y2+1, x1] - integral[y1, x2+1] + integral[y1, x1]

         window_area = (x2 - x1 + 1) * (y2 - y1 + 1)
         output[y, x] = sum_window / window_area 
  return output    
     

''' Calculate the time-structure matrix of an image pair.
 image im: the input image.
 image prev: the previous image in sequence.
 int s: window size for smoothing.
 returns: structure matrix. 1st channel is Ix^2, 2nd channel is Iy^2,
          3rd channel is IxIy, 4th channel is IxIt, 5th channel is IyIt.
'''
def time_structure_matrix(im, prev, s):
    im = im.astype(np.float32)
    prev = prev.astype(np.float32)
    Ix = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=3)
    Iy = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=3)
    It = prev - im

    return np.stack([
        box_filter_image(Ix * Ix, s),
        box_filter_image(Iy * Iy, s),
        box_filter_image(Ix * Iy, s),
        box_filter_image(Ix * It, s),
        box_filter_image(Iy * It, s),
    ], axis=-1)  

'''
Calculate the velocity given a structure image
image S: time-structure image
int stride: 
'''
def velocity_image(S, stride):
    h, w = S.shape[:2]
    v = np.zeros((h, w, 2), dtype=np.float32)

    for y in range(0, h, stride):
        for x in range(0, w, stride):
            Ix2, Iy2, IxIy, IxIt, IyIt = S[y, x]
            M = np.array([[Ix2, IxIy], [IxIy, Iy2]])
            b = np.array([-IxIt, -IyIt])

            if np.linalg.det(M) > 1e-5:
                v[y, x] = np.linalg.inv(M) @ b
    return v  

  
  
'''
Draw lines on an image given the velocity
image im: image to draw on
image v: velocity of each pixel
float scale: scalar to multiply velocity by for drawing
'''
def draw_flow(im, v, scale ):
    im = np.array(im)
    im_draw = im.copy()
    for y in range(0, im.shape[0], 8):
        for x in range(0, im.shape[1], 8):
            dx, dy = v[y, x] * scale
            if abs(dx) > 0.5 or abs(dy) > 0.5:
                pt1 = (x, y)
                pt2 = (int(x + dx), int(y + dy))
                cv2.arrowedLine(im_draw, pt1, pt2, (0, 255, 0), 1, tipLength=0.3)
    return im_draw  

'''
Constrain the absolute value of each image pixel
image im: image to constrain
float v: each pixel will be in range [-v, v]
'''
def constrain_image(im, v):
  return np.clip(im, -v, v)

'''
Calculate the optical flow between two images
image im: current image
image prev: previous image
int smooth: amount to smooth structure matrix by
int stride: downsampling for velocity matrix
returns: velocity matrix
'''
def optical_flow_images(im, prev, smooth, stride):
    if len(im.shape) > 2:
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
        prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY).astype(np.float32)
    else:
        im_gray = im.astype(np.float32)
        prev_gray = prev.astype(np.float32)
        
    if im.shape != prev.shape:
      im_gray = cv2.resize(im,(prev_gray.shape[1], prev_gray.shape[0])) 
    S = time_structure_matrix(im_gray, prev_gray, smooth)
    
    v = velocity_image(S, stride)
    
    return v
'''
Run optical flow demo on webcam
int smooth: amount to smooth structure matrix by
int stride: downsampling for velocity matrix
int div: downsampling factor for images from webcam
'''
def optical_flow_webcam(smooth, stride, div):
    frame_count = 0
    cap = cv2.VideoCapture(0)
    ret, prev = cap.read()
    prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_small = cv2.resize(gray, (gray.shape[1] // div, gray.shape[0] // div))

        prev_small = cv2.resize(prev, (prev.shape[1] // div, prev.shape[0] // div))

        flow = optical_flow_images(prev_small, gray_small, smooth, stride)
        flow_vis = draw_flow(cv2.resize(frame, gray_small.shape[::-1]), flow, 8)
        """cv2.imshow("Optical Flow", flow_vis)"""

        cv2.imshow("Optical Flow", cv2.resize(flow_vis, (flow_vis.shape[1] * 2, flow_vis.shape[0] * 2)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        prev = gray
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()  


def __main__():
  # usage
  # python flow_image.py --webcam --smooth 150 --stride 100 --div 30
  # python flow_image.py --images --img1 .\foto1.png --img2 .\foto2.png --output lines.png
  
    parser = argparse.ArgumentParser(description="Optical Flow Application")
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--images', action='store_true', help="Run optical flow on two images")
    mode_group.add_argument('--webcam', action='store_true', help="Run optical flow on webcam")
    
    parser.add_argument('--img1', type=str, help="Path to the first image (previous frame)")
    parser.add_argument('--img2', type=str, help="Path to the second image (current frame)")
    parser.add_argument('--output', type=str, default="lines.jpg", help="Output image path")
    
    parser.add_argument('--smooth', type=int, default=15, help="Smoothing window size")
    parser.add_argument('--stride', type=int, default=4, help="Stride for velocity calculation") 
    parser.add_argument('--div', type=int, default=4, help="Downsampling factor for webcam")    
    
    args = parser.parse_args()

    if args.images:
        if not args.img1 or not args.img2:
            print("Error: Both --img1 and --img2 must be provided in image mode")
            return
        img1 = cv2.imread(args.img1)
        img2 = cv2.imread(args.img2)
        
        if img1 is None:
            print(f"Error: Could not read image {args.img1}")
            return
            
        if img2 is None:
            print(f"Error: Could not read image {args.img2}")
            return
        
        flow = optical_flow_images(img2, img1, args.smooth, args.stride)
        
        result = draw_flow(img1, flow, args.stride)
        
        cv2.imshow("Optical Flow Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        cv2.imwrite(args.output, result)
        print(f"Saved result to {args.output}")
    
    elif args.webcam:
        print("Running webcam demo. Press ESC to exit.")
        optical_flow_webcam(args.smooth, args.stride, args.div)
    
if __name__ == "__main__":
    __main__()