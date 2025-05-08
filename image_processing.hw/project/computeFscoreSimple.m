function computeFscoreSimple(imageFolder, totalPlates)
% COMPUTEFSCORESIMPLE  Run detectPlateBoxes on a folder and compute
% precision, recall & F-score given totalPlates (one plate per image).
%
%   computeFscoreSimple('images', 62)

  files = dir(fullfile(imageFolder,'*.jpg'));
  N     = numel(files);

  if N ~= totalPlates
    warning('Found %d images but you told me there are %d plates. Using N_images = %d.', ...
            N, totalPlates, N);
    totalPlates = N;
  end

  totalRects        = 0;   % sum of all detected boxes
  imagesWithDetect  = 0;   % #images where detectPlateBoxes returned ≥1

  for i = 1:N
    imgPath = fullfile(imageFolder, files(i).name);
    I       = imread(imgPath);
    bboxes  = detectPlateBoxes(I);  % your original logic, unchanged

    numHere = size(bboxes,1);
    totalRects = totalRects + numHere;
    if numHere > 0
      imagesWithDetect = imagesWithDetect + 1;
    end
  end

  % Compute counts
  TP = imagesWithDetect;           % one correct plate per image with any detection
  FP = totalRects - TP;            % extra boxes beyond the first in each image
  FN = totalPlates - TP;           % images where detection==0

  % Avoid division by zero
  if TP + FP == 0
    precision = 0;
  else
    precision = TP / (TP + FP);
  end
  if TP + FN == 0
    recall = 0;
  else
    recall = TP / (TP + FN);
  end
  if precision+recall == 0
    Fscore = 0;
  else
    Fscore = 2 * (precision * recall) / (precision + recall);
  end

  % Display
  fprintf('\nAcross %d images (62 plates total):\n', N);
  fprintf('  True Positives : %d\n', TP);
  fprintf('  False Positives: %d\n', FP);
  fprintf('  False Negatives: %d\n\n', FN);
  fprintf('  Precision = %.2f%%\n', precision*100);
  fprintf('  Recall    = %.2f%%\n', recall*100);
  fprintf('  F-score   = %.2f%%\n\n', Fscore*100);
end
