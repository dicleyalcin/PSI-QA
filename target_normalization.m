% clear all;
%% global variables
class = "positive";
patient="AD44_raw_trimmed";

%% Reading the files
Files=dir(strcat('Z:\DicleYalcin\Amyloid Project\',patient,'\',class,'\*.jpg'));
Names={};
for k=1:length(Files)
    FileNames=Files(k).name;
    Names{k}=FileNames;
end

imagePathList=Names(1:end);


%% Picking the target image for normalization (positive, then positive)

% sourceImage=imread('Z:\DicleYalcin\Amyloid Project\AD46_raw_trimmed\positive\out_AD47-A7 Amyloid-APP ab11132 M1.jpg');
    % Extract the individual red, green, and blue color channels.
targetVectors = double.empty(length(imagePathList),0);
%1:length(imagePathList) 
for i=1:length(imagePathList) 
    imagePath=strcat('Z:\DicleYalcin\Amyloid Project\',patient,'\',class,'\',char(imagePathList(i)));
    titlename=char(imagePathList(i));
    rgbImage=imread(imagePath);
    redChannel = rgbImage(:, :, 1);
	greenChannel = rgbImage(:, :, 2);
	blueChannel = rgbImage(:, :, 3);
    pixelCountRed = imhist(redChannel, 255);
    pixelCountGreen = imhist(greenChannel, 255);
    pixelCountBlue = imhist(blueChannel, 255);
    subplot(20,20,i);
    lineWidth = 2;
	hold off;
	plot(pixelCountRed, 'r', 'LineWidth', lineWidth);
	hold on;
	grid on;
	plot(pixelCountGreen, 'g', 'LineWidth', lineWidth);
	plot(pixelCountBlue, 'b', 'LineWidth', lineWidth);
% 	title('All the Color Histograms (Superimposed)', 'FontSize', fontSize);
    set(gca, 'YScale', 'log');
    %xlim([200 255]);
    averageDist = mean(rescale([abs(max(pixelCountRed)-max(pixelCountGreen)) 
        abs(max(pixelCountRed)-max(pixelCountBlue))
        abs(max(pixelCountGreen)-max(pixelCountBlue))]));
    targetVectors(i)=averageDist;
end
targetPath = strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\',Files(targetVectors == min(targetVectors)).('name'))

%% once it's picked, we normalize (positive, then positive)
%% Reading the files
targetPath = 'Z:\\DicleYalcin\\Amyloid Project\\AD44_raw_trimmed\\positive\\out_AD44-A9 Tau P-T181 ab75679 Rab10.jpg';

Files=dir(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\*.jpg'));
Names={};
for k=1:length(Files)
    FileNames=Files(k).name;
    Names{k}=FileNames;
end

imagePathList=Names(1:end);
for i=1:length(imagePathList) 
    imagePath=strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\',char(imagePathList(i)));
    titlename=char(imagePathList(i));
    rgbImage=imread(imagePath);
    targetImage=imread(targetPath);
    norm = NormRGBHist(rgbImage,targetImage);
    
    [rows,columns,numberofColorChannels]=size(norm);

    % Get the rows and columns to split at,
    % Taking care to handle odd-size dimensions:
    col1 = 1;
    col2 = floor(columns/2);
    col3 = col2 + 1;
    row1 = 1;
    row2 = floor(rows/2);
    row3 = row2 + 1;
    % Now crop
    upperLeft = imcrop(norm, [col1 row1 col2 row2]);
    upperRight = imcrop(norm, [col3 row1 columns - col2 row2]);
    lowerLeft = imcrop(norm, [col1 row3 col2 row2]);
    lowerRight = imcrop(norm, [col3 row3 columns - col2 rows - row2]);
    
%     normPiece_1=norm(1:length(norm(:,1,:))/2,1:length(norm(1,:,:))/2 ,3);
%     normPiece_1=imcrop(norm,[]);
%     normPiece_2=norm(((length(norm(:,1,:))/2)+1):length(norm(:,1,:)),((length(norm(1,:,:))/2)+1):length(norm(1,:,:)),3);
    % ,'WriteMode','append'
    imwrite(upperLeft,sprintf(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\normalized\\NORM_%s_mainSub1.tif'),titlename(1:end-4)));
    imwrite(upperRight,sprintf(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\normalized\\NORM_%s_mainSub2.tif'),titlename(1:end-4)));
    imwrite(lowerLeft,sprintf(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\normalized\\NORM_%s_mainSub3.tif'),titlename(1:end-4)));
    imwrite(lowerRight,sprintf(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient,'\\',class,'\\normalized\\NORM_%s_mainSub4.tif'),titlename(1:end-4)));
    
end


