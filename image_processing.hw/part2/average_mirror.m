function out = average_mirror(img)
    img_mirror = img(:, end:-1:1);
    out = uint8((double(img) + double(img_mirror)) / 2); 
end
