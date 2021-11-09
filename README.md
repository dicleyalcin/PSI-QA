# WSIHistPathAnalysis
An Accurate and Unbiased Immunostaining Whole Slide Image Analysis Pipeline 

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
  * lxml
  ``` pip install lxml-4.6.3 ```
* imagemagick
  * For Linux users, use ``` sudo apt update && sudo apt install imagemagick ``` 
  * For Mac users, you may need to run ```conda install -c conda-forge imagemagick ```
