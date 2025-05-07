function out = flip_vertical(img)
    [rows, ~] = size(img);
    out = img(rows:-1:1, :); 
end
