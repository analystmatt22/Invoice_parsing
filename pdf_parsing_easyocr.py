# -*- coding: utf-8 -*-
"""PDF_parsing_easyocr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1izlYsxgR0h-jp5XGGXTwZReDtbtW8BBO

#### STEP 1: CONVERSION OF PDF INPUT TO JPG OUTPUT
"""

!pip install PyMuPDF

import fitz
from typing import Tuple
import os

def convert_pdf2img(input_file: str, pages: Tuple = None):
    """Converts pdf to image and generates a file by page"""
    # Open the document
    pdfIn = fitz.open(input_file)
    output_files = []
    # Iterate throughout the pages
    for pg in range(pdfIn.pageCount):
        if str(pages) != str(None):
            if str(pg) not in str(pages):
                continue
        # Select a page
        page = pdfIn[pg]
        rotate = int(0)
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable) = filesize large
        zoom_x = 2
        zoom_y = 2
        # The zoom factor is equal to 2 in order to make text clear
        # Pre-rotate is to rotate if needed.
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        output_file = f"{os.path.splitext(os.path.basename(input_file))[0]}_page{pg+1}.png"
        pix.writePNG(output_file)
        output_files.append(output_file)
    pdfIn.close()
    summary = {
        "File": input_file, "Pages": str(pages), "Output File(s)": str(output_files)
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return output_files

if __name__ == "__main__":
    import sys
    input_file = '/content/BYD-01.pdf' #sys.argv[1]
    convert_pdf2img(input_file)

"""### *We will get all pages converted to png format and saved as each file. Example: PDF with 4 pages will give 4 files of png*

#### STEP 2: EXTRACTION OF PURCHASE ORDER DATA FROM PDF TO EXCEL FILE
"""

!pip install easyocr
!pip install opencv-python

import matplotlib.pyplot as plt
import cv2
import easyocr

import pandas as pd
import numpy as np

from pylab import rcParams
from IPython.display import Image

reader = easyocr.Reader(['en'])

"""#### Text extraction of invoice"""

Image('/content/BYD-01_page1.png') #Selected specific page with the invoice, manually

#46 seconds for the code to run

invoice_data = reader.readtext('/content/BYD-01_page1.png') #reading the text
#output

df = pd.DataFrame(invoice_data) #creating a dataframe
df.rename(columns={0: 'Coordinates', 1: 'Strings',2: 'Accuracy'}, inplace=True) #renaming the columns
df.drop('Coordinates', inplace=True, axis=1)
df.to_excel("invoice_data.xlsx") #exporting to excel

Field = invoice_data[1][1]
Field

"""#### HIGHLIGHTING IN THE BOUNDING BOX"""

cord = output[1][0]
x_min, y_min = [min(idx) for idx in zip(*cord)]
x_max, y_max = [max(idx) for idx in zip(*cord)]

#Highlighting in the bounding box:

image = cv2.imread('/content/BYD-01_page4.png')
cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,0,255),2)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
rcParams['figure.figsize'] = 10,10

"""#### BOUNDING BOX DATA EXTRACTION

#####https://github.com/microsoft/unilm/blob/master/dit/requirements.txt
#####https://github.com/microsoft/unilm/tree/master/dit
"""

#Do the above links during free time

"""#### NEW GITHUB LINK: DO each step by step as shown

https://github.com/naiveHobo/InvoiceNet

https://gitlab.com/naiveHobo

https://www.linkedin.com/in/sarthak-mittal/
"""

!git clone https://github.com/naiveHobo/InvoiceNet.git

cd InvoiceNet/

!./install.sh

!source env/bin/activate

# Install InvoiceNet
!pip install .

# Create conda environment and activate
!conda create --name invoicenet python=3.7
!conda activate invoicenet

# Install poppler
!conda install -c conda-forge poppler

"""####Checking whether conda is installed

####https://inside-machinelearning.com/en/how-to-install-use-conda-on-google-colab/
"""

!conda --version #Checking the conda version

#installing conda

!pip install -q condacolab
import condacolab
condacolab.install()

!conda --version

!which conda #location of conda

!sudo pip install --upgrade google-api-python-client
!sudo pip install google-cloud-vision

#Conda-forge is a community effort that provides conda packages for a wide range of software.
# Install poppler
#!conda install -c conda-forge poppler

"""##Conversion of pdf to json format"""

#We need to convert the pdf to a json format and save in the folder train_data
#Names of the respective pdf and json shall be same
#This is a mandatory step before training the data

#To add your own fields to InvoiceNet, open invoicenet/__init__.py.
#FIELD_TYPES["general"] : General field like names, address, invoice number, etc.
#FIELD_TYPES["optional"] : Optional fields that might not be present in all invoices.
#FIELD_TYPES["amount"] : Fields that represent an amount.
#FIELD_TYPES["date"] : Fields that represent a date.

#Installing tesseract
!sudo apt install tesseract-ocr
!pip install pytesseract

#Prepare the data for training first by running the following command:
!python prepare_data.py --data_dir train_data/

#Train InvoiceNet using the following command:
# For example, for field 'total_amount'
!python train.py --field invoice_date --batch_size 8

!python predict.py --field invoice_date --data_dir predict_data/

"""https://bhadreshpsavani.medium.com/how-to-use-tesseract-library-for-ocr-in-google-colab-notebook-5da5470e4fe0"""

!sudo apt install tesseract-ocr
!pip install pytesseract

import pytesseract
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image

!pip list

from google.colab import files
uploaded = files.upload()

"""image_path_in_colab=‘image.jpg’

extractedInformation = pytesseract.image_to_string(Image.open(image_path_in_colab))

print(extractedInformation)
"""

image_path_in_colab= 'test_image.jpg'

extractedInformation = pytesseract.image_to_string(Image.open(/content/test_image.jpg))

print(extractedInformation)

# Get bounding box estimates
print(pytesseract.image_to_boxes(Image.open(/content/test_image.jpg)))



import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open("test_image.jpg") # the second one 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('temp2.jpg')
text = pytesseract.image_to_string(Image.open('temp2.jpg'))
print(text)

