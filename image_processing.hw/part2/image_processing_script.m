
img = imread('test_image.jpg');

if size(img, 3) == 3
    img_gray = rgb2gray(img);
    img_color = img; % Save original color image
else
    img_gray = img; % Image is already grayscale
    img_color = repmat(img_gray, [1,1,3]); 
end

img_flip_v = flip_vertical(img_gray);
img_flip_h = flip_horizontal(img_gray);
img_negative = negative_image(img_gray);
img_swap_rg = swap_red_green(img_color);
img_avg_mirror = average_mirror(img_gray);
img_random_noise = add_random_noise(img_gray);

figure;

subplot(2,3,1);
imshow(img_gray);
title('Original Image');

subplot(2,3,2);
imshow(img_flip_v);
title('Flipped Vertically');

subplot(2,3,3);
imshow(img_flip_h);
title('Flipped Horizontally');

subplot(2,3,4);
imshow(img_negative);
title('Negative Image');

subplot(2,3,5);
imshow(img_swap_rg);
title('Swap Red & Green');

subplot(2,3,6);
imshow(img_avg_mirror);
title('Average with Mirror');

figure;
imshow(img_random_noise);
title('Image with Random Noise');

