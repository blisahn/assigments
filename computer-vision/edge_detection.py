import argparse
import math
import cv2
import numpy as np

def smooth(image, kernel_size = 5):
    if kernel_size % 2 == 0:
        kernel_size += 1
    

    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    center = kernel_size // 2
    sigma = kernel_size / 6.0 
    total = 0
    for i in range(kernel_size):
        for j in range(kernel_size):
            x, y = i - center, j - center
            kernel[i, j] = math.exp(-(x*x + y*y) / (2 * sigma * sigma))
            total += kernel[i, j]

    kernel /= total

    height, width = image.shape[:2]
    pad = kernel_size // 2
    

    if len(image.shape) == 3: 
        padded = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REFLECT)
        result = np.zeros_like(image)
        
        for c in range(image.shape[2]):  
            for i in range(height):
                for j in range(width):
                    region = padded[i:i+kernel_size, j:j+kernel_size, c]
                    result[i, j, c] = np.sum(region * kernel)
    else: 
        padded = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REFLECT)
        result = np.zeros_like(image)
        
        for i in range(height):
            for j in range(width):
                region = padded[i:i+kernel_size, j:j+kernel_size]
                result[i, j] = np.sum(region * kernel)   
    return result
   
                



def conv2d(kernel_size = 2):
    return np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size * kernel_size)

def compute_gradients(image, output_name):
    height, width = image.shape[:2]
    kernel_size = 3
    smoothed_img = smooth(image, kernel_size)
    image = smoothed_img
    gray_img = np.zeros((height,width), dtype=np.uint8)


    for i in range(height):
        for j in range (width):
            r, g, b = image[i, j]
            gray_img[i, j] = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
                   

    cv2.imwrite("gray_dog_img.jpeg",gray_img) 
    
    horizontal_filter = [[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]]
    
    vertical_filter= [[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]]
    
    horizontal_gradient_img =  np.zeros((height, width), dtype=np.int16)
    vertical_gradient_img =   np.zeros((height, width), dtype=np.int16)

    padded_img = cv2.copyMakeBorder(gray_img, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
    

    for i in range(height):
        for j in range(width):
            region = padded_img[i:i+3, j:j+3]
            region = region.astype(np.int16)
            gx = 0
            gy = 0 
            
            for k in range(3):
                for l in range(3):
                    gx += region[k, l] * horizontal_filter[k][l]
                    gy += region[k, l] * vertical_filter[k][l]
                    
            horizontal_gradient_img [i, j] = gx
            vertical_gradient_img [i, j] = gy

    magnitude = np.zeros((height, width), dtype=np.float32)
    orientation = np.zeros((height, width), dtype=np.float32)

    for i in range(height):
        for j in range(width):
                gx = float(horizontal_gradient_img[i, j])  
                gy = float(vertical_gradient_img[i, j])
                mag_value = gx * gx + gy * gy 
                magnitude[i][j] = math.sqrt(mag_value)  
                if gx == 0:
                    orientation[i][j] = 90 if gy > 0 else -90 
                else:
                    angle = gy / gx  
                    orientation[i][j] = math.atan(angle) * (180 / math.pi)

    for i in range(height):
        for j in range(width):
            horizontal_gradient_img[i][j] = int(max(0, min(255, abs(horizontal_gradient_img[i][j]))))
            vertical_gradient_img[i][j] = int(max(0, min(255, abs(vertical_gradient_img[i][j]))))
            magnitude[i][j] = int(max(0, min(255, magnitude[i][j])))
            orientation[i][j] = int(max(0, min(255, (orientation[i][j] + 180) / 2))) 

    def save_image(filename, img):
        height, width = len(img), len(img[0])
        out_img = cv2.UMat(height, width, cv2.CV_8U)
        out_img = np.array(img, dtype=np.uint8)
        cv2.imwrite(filename, out_img)
        


    save_image(f"{output_name}_gx.png", horizontal_gradient_img)
    save_image(f"{output_name}_gy.png", vertical_gradient_img)
    save_image(f"{output_name}_grad.png", magnitude)
    save_image(f"{output_name}_orit.png", orientation)


    print(f"Saved gradient images as {output_name}_gx.png, {output_name}_gy.png, {output_name}_grad.png, {output_name}_orit.png")

    return magnitude, orientation

def tresholding(magnitude, low_thresh, high_thresh, output_name):
    height, width = magnitude.shape
    
    low_threshold_img = np.zeros((height, width), dtype=np.uint8)
    high_threshold_img = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            if magnitude[i, j] >= low_thresh:
                low_threshold_img[i, j] = 255
            if magnitude[i, j] >= high_thresh:
                high_threshold_img[i, j] = 255
                
    cv2.imwrite(f"{output_name}_low.png", low_threshold_img)
    cv2.imwrite(f"{output_name}_high.png", high_threshold_img)
    
    print(f"Saved threshold images as {output_name}_low.png and {output_name}_high.png")
    return low_threshold_img, high_threshold_img



def tracking(high_thresh_img, low_thresh_img, out_name):
    height, width = high_thresh_img.shape

    tracked = high_thresh_img.copy()

    dx = [-1, -1, -1,  0,  0,  1, 1, 1]
    dy = [-1,  0,  1, -1,  1, -1, 0, 1]

    strong_edges = []
    for i in range(height):
        for j in range(width):
            if high_thresh_img[i, j] == 255:
                strong_edges.append((i, j))

    while strong_edges:
        i, j = strong_edges.pop(0)
        
        for k in range(8):
            ni, nj = i + dx[k], j + dy[k]
            
            if 0 <= ni < height and 0 <= nj < width:
                if low_thresh_img[ni, nj] == 255 and tracked[ni, nj] == 0:
                    tracked[ni, nj] = 255
                    strong_edges.append((ni, nj))

    cv2.imwrite(f"{out_name}_track.png", tracked)
    print(f"Saved edge tracking image as {out_name}_track.png")
    
    return tracked

def edge_detection(img, low_thresh, high_thresh, output_name):
    print("edge detection calisio")
    smoothed = smooth(img, kernel_size=3)
    
    magnitude, orientation = compute_gradients(smoothed, output_name)
    
   
    low_img, high_img = tresholding(magnitude, low_thresh, high_thresh, output_name)
    

    final_edges = tracking(high_img, low_img, output_name)
    height, width, channels = img.shape
    laplacian_filter = [[0, -1, 0],
                        [-1, 4, -1],
                        [0, -1, 0]]
    output_im = np.zeros((height, width, channels), dtype=np.uint8)
    pad_size = 1
    padded_img = cv2.copyMakeBorder(img, pad_size, pad_size, pad_size, pad_size, cv2.BORDER_REFLECT) ## to avoid exceptions might be occur when u deal with edges and borders.
    for c in range (channels):
        for i in range (height):
            for j in range (width):
                copied_part = padded_img[i:i+3, j:j+3, c]
                copied_part = np.sum(copied_part * laplacian_filter)
                output_im[i,j,c] = 255 if copied_part > high_thresh else (0 if copied_part< low_thresh else copied_part)
    compute_gradients(img, output_name)
    output_filename = f"{output_name}_edgedetection.jpg"
    print(f"Saving image to: {output_filename}")
    cv2.imwrite(output_filename, output_im)

    return output_im

def __main__():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run image resizing.")

    # Required argument for the image filename
    parser.add_argument('img_name', type=str, help="Path to the input image")
    # Required argument for the output filename
    parser.add_argument('out_name', type=str, help="Path to the output image")

    # Canny edge detection threshold values (default values are provided)
    parser.add_argument('--low_thresh', type=int, default=50, help="Low threshold for Canny edge detection")
    parser.add_argument('--high_thresh', type=int, default=150, help="High threshold for Canny edge detection")

    args = parser.parse_args()

    # Load the image
    img = cv2.imread(args.img_name)
    resized_img = edge_detection(img, args.low_thresh, args.high_thresh, args.out_name)
    print("Completed!")


if __name__ == "__main__":
   __main__()

