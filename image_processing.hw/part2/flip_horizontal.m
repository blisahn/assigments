function out = flip_horizontal(img)
    [~, cols] = size(img);
    out = img(:, cols:-1:1); 
end
