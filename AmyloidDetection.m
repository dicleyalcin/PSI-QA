% load('ADproject_data.mat')

lookup=lookupAD22;
patient_dir="AD22_raw_trimmed";
outpat_dir="masked";



Files=dir(strcat('Z:\DicleYalcin\Amyloid Project\',patient_dir,'\splitted\*.jpg'));
Names={};
for k=1:length(Files)
   FileNames=Files(k).name;
   Names{k} = FileNames;
end

 
strs=[];
for i=1:length(Names)  
    region=char(Names(i));
    RegionIndex=strfind(region,"A");
    RegionIndex=RegionIndex(3);
    SubRegionIndex=strfind(region,"M");
    srendIndex=strfind(region,"_mainSub");
    srstartIndex=strfind(region," Amyloid-");
    SubRegionIndex=SubRegionIndex(2);
    strcompare = "A"+region(RegionIndex+1:srstartIndex-1)+"M"+region(SubRegionIndex+1:srendIndex-1);
    strs = [strs; strcompare];
end

[v, w] = unique( strs, 'stable' );
w(end+1)=length(strs)+1;
duplicate_indices = setdiff( 1:numel(strs), w );


sizeGroupMinDiff = 14;
PAI_bootstrapped = [];
for b=1:10
    b
    imagePathList={};
    for j=1:length(lookup)
        if lookup{j,1}=="absent"
            imagePathList{j}="absent";
        else      
            newStr = split(lookup{j,1},',');
            bigGroup = {};
            for i=1:length(w)-1
                group = Names(w(i):w(i+1)-1);
                for k=1:length(group)
                    groupElement=group(k);
                    region=char(groupElement);
                    RegionIndex=strfind(region,"A");
                    RegionIndex=RegionIndex(3);
                    SubRegionIndex=strfind(region,"M");
                    srendIndex=strfind(region,"_mainSub");
                    srstartIndex=strfind(region," Amyloid-");
                    SubRegionIndex=SubRegionIndex(2);
                    strcompare = "A"+region(RegionIndex+1:srstartIndex-1)+"M"+region(SubRegionIndex+1:srendIndex-1);          
                    if sum(ismember(newStr,strcompare))
                        bigGroup = cat(2,bigGroup,group(k)); 
                    end             
                end        
            end
            length(bigGroup);
            msize = numel(bigGroup);
            elements = bigGroup(randperm(msize, sizeGroupMinDiff));
            imagePathList{j}=elements;  
        end
    end           

    imagePathList = horzcat(imagePathList{:});
    imagePathList(ismember(imagePathList,"absent")) = [];


    % Read and Check Image Dimensions
    percentInts = [];
    for i=1:length(imagePathList) 
        imagePath = strcat('Z:\DicleYalcin\Amyloid Project\',patient_dir,'\splitted\',char(imagePathList(i)));

        titlename=char(imagePathList(i));
        rgbImage = imread(imagePath);  
        
        imwrite(rgbImage,sprintf(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient_dir,'\\',outpat_dir,'\\original\\resultMaskedORIGINAL_%s.tif'),titlename(1:end-4)));
        
        
    %     h=figure;
    %     set(h,'visible','off');
    %     subplot(1,2,1);
    %     imshow(rgbImage, []);
    %     title('Original Color Image', 'FontSize', fontSize);       
        % Get the dimensions of the image.  numberOfColorBands should be = 3.
        % Convert to hsv color space.
        hsv = rgb2hsv(rgbImage);
        % Display the color channels.
        hueImage = hsv(:, :, 1);
        saturationImage = hsv(:, :, 2);
        valueImage = hsv(:, :, 3);


        redChannel = rgbImage(:,:,1);
        greenChannel = rgbImage(:,:,2);
        blueChannel = rgbImage(:,:,3);

        clear Rs Gs Bs;
        Rs(:,:) = rgbImage(:,:,1);
        Gs(:,:) = rgbImage(:,:,2);
        Bs(:,:) = rgbImage(:,:,3);



        bThreshL=210;
        bThreshH=245;
        filterBlack = 25;
        filterWhite = 200;




    %     subplot(1,2,2);

        mask = (redChannel > 0) & (blueChannel < 150) & (greenChannel > 0);
%         mask = (redChannel > 0) & (blueChannel < 160) & (greenChannel > 30);

%         mask = (redChannel > 100) & ((blueChannel < bThreshL) | (blueChannel > bThreshH) ) & (greenChannel > 100);


        maskedRgbImage = bsxfun(@times, rgbImage, cast(mask,class(rgbImage)));
    %     imshow(maskedRgbImage);
    %     title('Masked Original Image','FontSize',fontSize)


        BW = rgb2gray(maskedRgbImage);

    %     subplot(1,4,3);
    %     imshow(BW);

    %     title('Grayscale converted Image','FontSize',fontSize)


    %     subplot(1,4,4);
        thresholdedBin = BW>1;
        imwrite(thresholdedBin,sprintf(strcat('Z:\\DicleYalcin\\Amyloid Project\\',patient_dir,'\\',outpat_dir,'\\masked\\resultMasked_%s.tif'),titlename(1:end-4)));





    %     imshow(thresholdedBin);


    %     title('Final Binarized Image','FontSize',fontSize);

        clear mRs mGs mBs;
        mRs(:,:) = maskedRgbImage(:,:,1);
        mGs(:,:) = maskedRgbImage(:,:,2);
        mBs(:,:) = maskedRgbImage(:,:,3); 

        % Enlarge figure to full screen.
    %     set(gcf, 'units','normalized','outerposition',[0 0 1 1]);    
    %     print(h,sprintf('Z:\\DicleYalcin\\Amyloid Project\\testCases\\results\\FIG_%s',titlename),'-dpng','-r400'); % will create FIG1, FIG2,...    

        percentInts = [percentInts; (sum(thresholdedBin(:))/sum(~thresholdedBin(:)))*100];

    end
    % figure;
    % PAI=[];
    % for i=1:5:length(Names)
    %    figure;
    %    bar(percentInts(i:i+4));
    %    Names(i)

    %    PAI=[PAI; mean(percentInts(i:i+4))];
    % end

    strs=[];
    for i=1:length(imagePathList)  
        region=char(imagePathList(i));
        RegionIndex=strfind(region,"A");
        RegionIndex=RegionIndex(3);
        SubRegionIndex=strfind(region,"M");
        srendIndex=strfind(region,"_mainSub");
        srstartIndex=strfind(region," Amyloid-");
        SubRegionIndex=SubRegionIndex(2);
        strcompare = "A"+region(RegionIndex+1:srstartIndex-1)+"M"+region(SubRegionIndex+1:srendIndex-1);
        strs = [strs; strcompare];
    end

    PAI=[];

    for j=1:length(lookup) % 
        if lookup{j}=="absent"
            PAI(j)=NaN;
        end
        newStr = split(lookup{j,1},',');
        avgdata=[];
        for i=1:length(strs) % 40 for AD47
            if sum(ismember(newStr,strs(i)))
                avgdata=[avgdata; percentInts(i)];
            end
        end
        PAI(j)=mean(avgdata);
    end
    PAI_bootstrapped=[PAI_bootstrapped; PAI];
end


PAI_AD22_new2 = PAI_bootstrapped';

finhm=heatmap(PAI_AD45_original,'Colormap',redbluecmap(100),'ColorScaling','log','grid','off','MissingDataColor','#808080','ColorbarVisible','on');
finhm.Title='AD45 (Tau+) Randomization Trials';
finhm.XDisplayLabels = {'R_1','R_2','R_3','R_4','R_5','R_6','R_7','R_8','R_9','R_{10}'};
s=struct(finhm);
s.XAxis.TickLabelRotation=90;
finhm.YDisplayLabels=labY;



% PAI_AD22_2=PAI_bootstrapped';
% 

% 
% % PAI_AD47_2([21,33],:)=[];
% % PAI_AD46_2([2,6,19,20,21,22,33],:)=[];
% % PAI_AD22_2([2,33,34],:)=[];
% rowlab={'R_1','R_2','R_3','R_4','R_5','R_6','R_7','R_8','R_9','R_{10}'};
% collab=strrep(cellstr(AmyloidMetadata(:,5)),'_','\_');
% collab([21,33],:)=[];
% % collab([2,6,19,20,21,22,33],:)=[];
% % collab([2,33,34],:)=[];
% rnames={'A11','A12','A2','A3','A41','A42','A5','A6','A7','A8','A91','A92','A93','A94','A95','A96','A97','A98','A99','A910','A911','A912','A101','A102','A103','A104','A105','A106','A107','A108','A109','A110','A1011','A1012','A111','A121','A122','A13','A14','A15','A16','A17'};
% rnames(:,[21,33])=[];
% % rnames(:,[2,6,19,20,21,22,33])=[];
% % rnames(:,[2,33,34])=[];
% % collabs={'A1_Superior frontal Lobe','A1_Middle frontal Lobe','A2_Anterior cingulate Lobe','A3_Anterior basal ganglia','A4_Superior temporal Lobe','A4_Middle temporal Lobe','A5_Globus pallidus','A6_Posterior basal ganglia + Hypothalamus','A7_Amygdala','A8_Thalamus','A9_CA4','A9_CA3','A9_CA2','A9_CA1','A9_Subiculum','A9_Entorhinal cortex','A9_Para-hippocampal gyrus','A9_Para-hippocampal Sulci','A9_Fusiform Sulci','A9_Fusiform Gyri','A9_Hippocampal fimbria','A10_CA4','A10_CA3','A10_CA2','A10_CA1','A10_Subiculum','A10_Entorhinal cortex','A10_Para-hippocampal gyrus','A10_Para-hippocampal Sulci','A10_Fusiform Sulci','A10_Fusiform Gyri','A10_Hippocampal fimbria','A11_Primary motor cortex','A12_Striate area','A12_Occipital gyrus','A13_Parietal Lobe','A14_Dentate nucleus','A15_Midbrain','A16_Pons','A17_Medulla oblongata'};
% % rm = struct('Labels',collab,'Colors',{"r","r","r","g","r","r","g","g","r","g","r","g","g","r","r","r","r","r","r","r","r","g","g","g","r","r","r","r","r","r","r","g","r","r","r","r","g","g","g","g"});
% llab={'r','r','r','g','r','r','g','g','r','g','r','g','g','r','r','r','r','r','r','r','r','g','g','g','r','r','r','r','r','r','r','g','r','r','r','r','g','g','g','g'};
% % llab={'r','r','g','r','g','g','r','g','g','g','g','r','r','r','r','r','g','g','g','g','g','g','r','r','r','r','g','g','g','g','r','g','g','g','g'};
% % llab={'r','g','g','r','r','g','g','r','g','g','g','g','g','g','r','r','r','r','r','r','g','g','g','g','g','g','r','r','r','g','g','g','g','g','r','g','g','g','g'};
% rm = struct('Labels',rnames,'Colors',llab);
% rm2 = struct('Labels',collab','Colors',llab);
% 
% c=clustergram(flipud(PAI_AD47_2),'Colormap',redbluecmap,'Cluster','all','Standardize','Column','RowLabels',flip(rnames'),'ColumnLabels',rowlab,'ColumnLabelsRotate',0,'RowLabelsColor',rm,'LabelsWithMarkers',true);
% % c=clustergram(flipud(PAI_AD47_2),'Colormap',redbluecmap,'Cluster','Row','Standardize','Column','RowLabels',flip(rnames'),'ColumnLabels',rowlab,'ColumnLabelsRotate',0,'RowLabelsColor',rm,'LabelsWithMarkers',true);
% % c=clustergram(flipud(PAI_AD22_2),'Colormap',redbluecmap,'Cluster','Row','Standardize','Column','RowLabels',flip(rnames'),'ColumnLabels',rowlab,'ColumnLabelsRotate',0,'RowLabelsColor',rm,'LabelsWithMarkers',true);
% 
% 
% % h2=HeatMap(flipud(PAI_AD47_2),'Colormap',redbluecmap,'Standardize','Column','RowLabels',flip(rnames'),'ColumnLabels',rowlab,'ColumnLabelsRotate',0,'RowLabelsColor',flipud(rm),'LabelsWithMarkers',true);






% figure;
% h=heatmap(PAI_AD47_2,'MissingDataColor','#808080','ColorbarVisible','on');
% h.ColorScaling = 'scaled';
% h.Title = 'AD47 randomization trials';
% h.Colormap = turbo(10);
% labY =  strrep(cellstr(AmyloidMetadata(:,5)),'_','\_');
% h.YDisplayLabels  = labY;
% h.XDisplayLabels = {'R_1','R_2','R_3','R_4','R_5','R_6','R_7','R_8','R_9','R_{10}'};
% % s = struct(h);
% % s.YAxis.TickLabelRotation = 90;  % vertical
% % s.XAxis.TickLabelRotation = 60;  % angled
% % s.XAxis.TickLabelRotation = 0;   % horizontal




% M=PAI_AD47_2';
% namedrows = categorical(roi_order);
% boxchart(PAI_AD47_2','Notch','on','BoxFaceColor','#EDB120')
% set(gca, 'XDir','reverse')
% set(gca,'XTick',1:42,'XTickLabel',namedrows)
% ylabel('Average Amyloid Intensity (%)')
% hold on;
% plot(mean(PAI_AD47_2');
% boxplot(PAI_AD47_2''Labels',strrep(labY,'\',''),'LabelOrientation','inline','Notch','off','Widths',0.6,'Orientation','horizontal')


    
% h=heatmap(mean(PAI_AD47_2')','MissingDataColor','#808080');
% h.ColorScaling = 'scaled';
% h.Title = 'AD47 randomization trials -- grand average';
% h.Colormap = parula(100);
% labY =  strrep(cellstr(AmyloidMetadata(:,5)),'_','\_');
% h.YDisplayLabels  = labY;

