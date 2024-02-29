% Lab: Light-sheet microscopy lab
% Physics and Astronomy Department, UNM
% Principal Investigator: Prof. Tonmoy Chakraborty

%addpath('Parallel_TIFF_Reader\getImageSize_mex\')
%addpath('Parallel_TIFF_Reader\parallelReadTiff\')
%%
clc, clear, close all,
datapath = '\Specify low resolution image directory\';
% Specify a score to distinguish the images
minscore = 0.1;

%%
answer = inputdlg({'How many positions?'});
NumPosition = str2num(answer{1});

%%
tic
score = zeros(1,NumPosition);
score_acc=[];
score_rej=[];
%% Creating text files
fName_acc = fopen('Locations_accepted.txt','wt');
fName_rej = fopen('Locations_rejected.txt','wt');
posL = zeros(3,NumPosition);
for nn = 1:NumPosition
    datapathPos = strcat(datapath,'position '," ", num2str(nn));
    
addpath(datapathPos);
%% Analyzing Images

filepath = dir(fullfile(datapathPos, '*.tif'));

tiff_info = imfinfo(filepath.name); % return tiff structure, one element per image
xsz = tiff_info(1).Width;
ysz = tiff_info(1).Height;
fmax = length(tiff_info);

ims = zeros(ysz,xsz,fmax,'uint16');
for ii = 1 : fmax
    ims(:,:,ii) = imread(filepath.name, ii);
end
    
ims = max(ims, [], 3);
sz = 20;
ims(ims<0) = min(abs(ims(:)));
thresh = 2.5;
im_unif = unif(ims, [sz sz],'rectangular') - unif(ims, [2*sz 2*sz],'rectangular');
im_max = (im_unif > thresh);
    
score(nn) = sum(im_max)/xsz/ysz*100; %
%images(:,:,nn) = ims;
disp(strcat('Finished ckecking image # ',num2str(nn)))
clear im_unif im_max

fName1 = fopen('AcqInfo.txt', 'r');

fid=fopen('AcqInfo.txt', 'r');
tline = fgetl(fid);
tlines = cell(0,1);

while ischar(tline)
    tlines{end+1,1} = tline;
    tline = fgetl(fid);
end
fclose(fid);

% Find the tlines with equations on them
eqnLines = regexp(tlines, '_mm =', 'match', 'once');
eqnLineMask = ~cellfun(@isempty, eqnLines);

% Convert the non equation lines to the second numeric value
k=0;
for i = find(eqnLineMask)'
    k=k+1;
    s=tlines{i};
    match=(regexp(s,'=','split'));
    pos(k)=str2num(match{1,2});
end
posL(:,nn) = pos;
fclose(fName1);

%%
if score(nn) >= minscore
   score_acc=[score_acc,score(nn)];
%  positions = [num2str(nn) '\t' num2str(nn) '\t' num2str(pos(1)) '\t' num2str(pos(2)) '\t' num2str(pos(3)) '\t' 'NaN' '\t' 'NaN'];
   positions = [num2str(numel(score_acc)) '\t' num2str(numel(score_acc)) '\t' num2str(pos(1)) '\t' num2str(pos(2)) '\t' num2str(pos(3)) '\t' 'NaN' '\t' 'NaN'];
   fprintf(fName_acc,positions);
   fprintf(fName_acc,'\n');
else
   score_rej=[score_rej,score(nn)];
%  positions = [num2str(nn) '\t' num2str(nn+1) '\t' num2str(pos(1)) '\t' num2str(pos(2)) '\t' num2str(pos(3)) '\t' 'NaN' '\t' 'NaN'];
   positions = [num2str(nn) '\t' num2str(nn) '\t' num2str(pos(1)) '\t' num2str(pos(2)) '\t' num2str(pos(3)) '\t' 'NaN' '\t' 'NaN'];
   fprintf(fName_rej,positions);
   fprintf(fName_rej,'\n');
end
rmpath(datapathPos)
end

ind_rej = find(score<minscore); % find rejected region
ind_acc = find(score>=minscore); % find accepted region

%figure;plot(score,'o-');hold on
%figure;plot(ind_rej,score(ind_rej),'o','LineWidth',2);

%dipshow(images(:,:,ind_rej))

%dipshow(images(:,:,ind_acc))

%%
mask = score < 0.5;
figure;
%scatter3(posL(1,:),posL(2,:),posL(3,:),(score+0.01)*10);hold on;
scatter3(posL(1,mask),posL(2,mask),posL(3,mask),(score(mask)+0.01)*30);hold on;
%scatter3(posL(1,~mask),posL(2,~mask),posL(3,~mask),(score(~mask)+0.01)*10);hold on;

axis equal
ind = [1:NumPosition];
figure;plot(ind(mask), score(mask),'.')
figure;plot(ind(~mask), score(~mask),'.')
toc
