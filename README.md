# PSIA
An Accurate and Unbiased Pathology Immunostaining Whole Slide Image Analysis Pipeline 

### Prerequisites & Installation Requirements

Pipeline run and tested on a Linux machine using Python 3.7.5 with 64-bit (Conda environment)

You can use ``` pip install -r requirements.txt ``` to install all the Python libraries required for running the project. These are detailed below if needed to be installed separately.

* Python libraries
  * OpenCV-Python
  ``` pip install opencv-python```
  or 
  ``` conda install opencv-python```
  * openslide library
  ``` pip install openslide-python ```
      * For Windows users, please download and extract the most recent stable openslide binary into your workspace directory, and change line 12 of ```WSI_to_ROIs.py``` to rename the directory name. 
  * lxml
  ``` pip install lxml ```
* imagemagick
  * For Linux users, use ``` sudo apt update && sudo apt install imagemagick ``` 
  * For Mac users, you may need to run ```conda install -c conda-forge imagemagick ```
* sckit-image
``` pip install sckit-image ```
* os
* numpy
* string
* matplotlib
### 1. fileProcess.py
### 2. WSI_to_ROIs.py
### 3. ROI_preprocess.py
