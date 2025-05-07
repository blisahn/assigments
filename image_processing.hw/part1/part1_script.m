A = randi([0, 255], 100, 100);

sorted_intensities = sort(A(:), 'descend');
figure;
plot(sorted_intensities);
title('Sorted Intensities in Decreasing Order');
xlabel('Index');
ylabel('Intensity');


t = 128; 
RGB = zeros(100, 100, 3);
RGB(:,:,1) = 255 * (A > t); 
imshow(uint8(RGB)); 


X = A(1:50, 1:50); 


A_mean = mean(A(:));
A_new = A - A_mean;


y = 1:12;
z = reshape(y, [4, 3]); 


v = [1 8 8 2 1 3 9 8]; 
x = sum(v == 8); 
