% load('ADproject_data.mat')
%% Reading the files
stain="Tau";
patient_dir="AD44_raw_trimmed";
lookup=lookupAD44;

Files=dir(strcat('Z:\DicleYalcin\Amyloid Project\',patient_dir,'\splitted\*.jpg'));
Names={};
for k=1:length(Files)
    FileNames=Files(k).name;
    Names{k}=FileNames;
end
imagePathList=Names(1:end);

%% Count the subsamples generated for each unique sub-region. Multiple regions with the same color code are merged.
% The minimum overlapping images are randomly chosen 
% Paths of these images are also necessary -- so we can pick them randomly
% How many will we pick? Depends on the min of subsampleCounts array.


subsets = [];
for i=1:length(lookup)
    newStr = split(lookup{i,1},',');
    count=[];
    for j=1:length(Names)
        region=char(Names(j));
        RegionIndex=strfind(region,"A");
        RegionIndex=RegionIndex(3);
        if stain=="Amyloid"
            SubRegionIndex=strfind(region,"M");
            srendIndex=strfind(region,"_mainSub");
            srstartIndex=strfind(region," Amyloid-");
            SubRegionIndex=SubRegionIndex(2);
            strcompare = "A"+region(RegionIndex+1:srstartIndex-1)+"M"+region(SubRegionIndex+1:srendIndex-1);
        end
        if stain=="Tau"
            SubRegionIndex=strfind(region,"Rab");
            srendIndex=strfind(region,"_mainSub");
            srstartIndex=strfind(region," Tau ");
            strcompare = "A"+region(RegionIndex+1:srstartIndex-1)+"Rab"+region(SubRegionIndex+3:srendIndex-1);            
        end
        if stain=="Tau2"
            SubRegionIndex=strfind(region,"Rab");
            srendIndex=strfind(region,"_mainSub");
            srstartIndex=strfind(region," Tau ");
            strcompare = "A"+region(RegionIndex+1:srstartIndex-1)+"Rab"+region(SubRegionIndex+3:srendIndex-1);            
        end        
        if sum(ismember(newStr,strcompare))
            count = [count; 1];
        end
    end
    subsets = [subsets; sum(count)]
end
out=min(setdiff(subsets,min(subsets)));