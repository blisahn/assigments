% detectPlateBoxes.m
function plateRects = detectPlateBoxes(rgbImage)
% DETECTPLATEBOXES  Return [x y w h] boxes for license-plate candidates.
%
% Uses the same area, aspect, extent, minor-axis, histogram and
% “letter-count” checks you had in your script.

  %-- 1) Greyscale & sharpen ---------------------------------------------
  grayImg   = rgb2gray(rgbImage);
  sharpGray = imsharpen(grayImg);

  %-- 2) Edge detection -------------------------------------------------
  edgeMask = edge(sharpGray, 'Canny');

  %-- 3) CC + region stats ----------------------------------------------
  cc    = bwconncomp(edgeMask);
  stats = regionprops(cc, ...
           'BoundingBox','Area','Extent','MinorAxisLength');

  plateRects = [];

  for k = 1:numel(stats)
    bb = stats(k).BoundingBox;    % [x y w h]
    A  = stats(k).Area;
    E  = stats(k).Extent;
    mL = stats(k).MinorAxisLength;
    w  = bb(3);  h = bb(4);

    %---- your original plate-shape tests -------------------------------
    if A > 100               && ...
       w > 2*h                && w < 7*h && ...
       E > 0.03               && ...
       mL > h

      %-- 4) Crop, binarize, filter, invert ----------------------------
      cropGray = imcrop(grayImg, bb);
      bwPlate  = imbinarize(cropGray);
      bwPlate  = medfilt2(bwPlate);
      bwPlate  = ~bwPlate;

      %-- 5) Histogram check ---------------------------------------------
      hCounts = imhist(bwPlate);

      %-- 6) Letter-shape test -------------------------------------------
      charCC    = bwconncomp(bwPlate);
      charStats = regionprops(charCC,'BoundingBox','Image');
      [Hpl, Wpl] = size(bwPlate);
      letterCount = 0;

      for c = 1:numel(charStats)
        imgC = charStats(c).Image;
        wC   = size(imgC,2);
        hC   = size(imgC,1);
        if wC < (Hpl/2) && hC > (Hpl/3)
          letterCount = letterCount + 1;
        end
      end

      %-- 7) Final histogram thresholds + letter presence ---------------
      if letterCount > 0 && ...
         hCounts(1) >  500 && hCounts(2) >  500 && ...
         hCounts(1) < 4000 && hCounts(2) < 4000

        plateRects = [plateRects; bb];
      end
    end
  end
end
