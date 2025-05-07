import argparse
import cv2
import numpy as np
import math


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
 

def nn_interpolate(im, c, h, w):
    # print("nn_intepolate calistij")
    #
    ## im input image path
    ## c channel index
    ## h target height
    ## w target width

    int_height = int(round(h))
    int_width = int(round(w))

    height, width = im.shape[:2]

    int_height = max(0, min(int_height, height - 1))
    int_width = max(0, min(int_width, width - 1))
    return im[int_height, int_width, c]




def nn_resize(im, h, w, out_name):
    # print("nn_Resize calisti")
   
    height, width, channels = im.shape
    output_im = np.zeros((h, w, channels), dtype=np.uint8)
    
    h_scale = height / h
    w_scale = width / w
    

    for i in range(h):
        for j in range(w):
            orig_i = i * h_scale
            orig_j = j * w_scale
            for c in range(channels):
                ##orig_i and orig_j are floating point numbers, so to estimate a valid image index they need to be rounded and casted
                # in nn_interpolate part.
                output_im[i, j, c] = nn_interpolate(im, c, orig_i, orig_j)
            # print(i * j)    
    
    output_filename = f"{out_name}_nn.jpg"
    print(f"Saving image to: {output_filename}")
    cv2.imwrite(output_filename, output_im)

    #write the image in this format: '%s_bilinear' % out_name
    return output_im


def bilinear_interpolate(im, c, h, w):
    # TODO
    height, width = im.shape[:2]
    ## retreiving the pixel coordinates 
    h1 = int(np.floor(h))
    w1 = int(np.floor(w))
    h2 = min(h1 + 1, height - 1)  # Hata önleme: Son satırı aşmayalım
    w2 = min(w1 + 1, width - 1)  

    a = h - h1
    b = w - w1

    point1 = float(im[h1, w1, c])
    point2 = float(im[h1, w2, c])
    point3 = float(im[h2, w1, c])
    point4 = float(im[h2, w2, c])

    top = point1 * (1 - b) + point2 * b
    bottom = point3 * (1 - b) + point4 * b

    horizontal = top * (1 - a) + bottom * a
    return int(round(horizontal))


def bilinear_resize(im, h, w, out_name):
    # TODO
    #write the image in this format: '%s_bilinear' % out_name
    height, width, channels = im.shape


    output_im = np.zeros((h, w, channels), dtype=np.uint8)

    h_scale = height / h
    w_scale = width / w


    for i in range(h):
        for j in range(w):
            orig_i = i * h_scale
            orig_j = j * w_scale
            for c in range(channels):
                output_im[i, j, c] = bilinear_interpolate(im, c, orig_i, orig_j)

    output_filename = f"{out_name}_bilinear.jpg"
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

    # Optional arguments for resizing dimensions
    parser.add_argument('--width', type=int, default=None, help="Width of the resized image")
    parser.add_argument('--height', type=int, default=None, help="Height of the resized image")

    # Choose between Nearest Neighbor (nn) and Bilinear (bilinear) resizing
    parser.add_argument('--resize_method', type=str, choices=['nn', 'bilinear'], default='nn', help="Resizing method to use")

    args = parser.parse_args()

    # Load the image
    img = cv2.imread(args.img_name)
    smoothed_img = smooth(img, 5)
    if args.width and args.height:
        resized_img = nn_resize(smoothed_img, args.height, args.width, args.out_name)
        print("Resized image using Nearest-Neighbor interpolation.")
        resized_img = bilinear_resize(smoothed_img, args.height, args.width, args.out_name)
        print("Resized image using Bilinear interpolation.")

if __name__ == "__main__":
   __main__()
