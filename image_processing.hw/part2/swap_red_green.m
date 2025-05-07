function out = swap_red_green(img)
    out = img;
    out(:,:,1) = img(:,:,2);
    out(:,:,2) = img(:,:,1);
end
