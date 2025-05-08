% runDetectionSequential.m
function runDetectionSequential(imageFolder)
% PROCESS & DISPLAY  Batch-process all .jpg’s in imageFolder, then
% show each with green boxes, one figure at a time, waiting for your key.

  files = dir(fullfile(imageFolder,'*.jpg'));
  N     = numel(files);
  results(N).image   = [];
  results(N).bboxes  = [];
  results(N).name    = '';

  %=== Stage 1: process all images =====================================
  for i = 1:N
    I    = imread(fullfile(imageFolder, files(i).name));
    bb   = detectPlateBoxes(I);
    results(i).image  = I;
    results(i).bboxes = bb;
    results(i).name   = files(i).name;
  end

  %=== Stage 2: show one at a time =====================================
  for i = 1:N
    clf;
    hFig = figure('Name',results(i).name,'NumberTitle','off');
    imshow(results(i).image); hold on
    for j = 1:size(results(i).bboxes,1)
      rectangle('Position',results(i).bboxes(j,:), ...
                'EdgeColor','g','LineWidth',3);
    end
    title(sprintf('Image %d/%d — %d plates detected', ...
           i, N, size(results(i).bboxes,1)), ...
           'Interpreter','none');
    pause;    % hit any key to continue
    close(hFig)
  end

  % assume totalTP, totalFP, totalFN have been accumulated
    precision = totalTP / ( totalTP + totalFP );   % correct detections / all detections
    recall    = totalTP / ( totalTP + totalFN );   % correct detections / all true plates

    Fscore = 2 * (precision * recall) / (precision + recall);

    fprintf('Precision = %.2f%%\n', precision*100);
    fprintf('Recall    = %.2f%%\n', recall*100);
    fprintf('F-score   = %.2f%%\n', Fscore*100);

end
