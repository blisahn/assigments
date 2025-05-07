function out = add_random_noise(img)
    noise = randi([-255, 255], size(img));
    img_noisy = double(img) + noise;
    img_noisy = max(0, min(255, img_noisy));
    out = uint8(img_noisy);
end
