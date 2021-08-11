"""
This script converts a directory (or several directories) of TIFFs to a 
single PDF. It uses the Pillow PIL fork library to load and compress TIFFs 
before saving them as a single PDF. It is adapted from a previous version of
the script that used ImageMagick for image handling, but Pillow handles these
tasks much more quickly. Because Pillow uses JPEG compression to reduce the
size of the PDF file output, the resulting PDFs may or may not be considered
suitable for publishing.

To run the script on a single directory of TIFFs, run the script as: 
    "python tiffs_to_pdf.py <path_to_folder>"

To run the script recursively on several directories, each containing TIFFs, 
run the following:
    "python tiffs_to_pdf.py <path_to_root_folder> -r"

When run recursively, the script will identify any folders containing TIFF 
files and create a PDF one directory above the TIFFs themselves. The PDF file
will be named according to the folder containing the TIFFs. If that folder is
named "TIFF", "TIFFs", "Master", or "Masters", the PDF will be given the name 
of that folder's parent folder, in an attempt to capture the object name for
the PDF. Additional "generic" folder names to be ignored can be added to the 
"genericTest" list on line 69.

"""


import sys
import os
import re
from PIL import Image

if not len(sys.argv) >= 2:
    print('Usage: python tiff_to_pdf_uncompressed.py <path_to_folder>')
    sys.exit('To run recursively on several subdirectories: python tiff_to_pdf_uncompressed.py <path_to_root_folder> -r')

if len(sys.argv) == 2:
    tiffsList = []
    folderPath = sys.argv[1]
    folderPath = folderPath.replace('\\', '/')
    folderName = folderPath.split('/')[-1]
    pdfPath = folderPath + '/' + folderName + '.pdf'
    fileList = os.listdir(folderPath)
    for file in fileList:
        if file.lower().endswith('.tif'):
            tiffsList.append(folderPath + '/' + file)
    tiffsList.sort()
    imageList = []
    for tiff in tiffsList:
        imageList.append(Image.open(tiff))
    imageList[0].save(pdfPath, save_all=True, append_images=imageList[1:])
        

elif sys.argv[2] == '-r':
    rootFolder = sys.argv[1]
    rootFolder = rootFolder.replace('\\','/')
    tiffFolders = []
    for root, dirs, files in os.walk(rootFolder):
        for file in files:
            if file.lower().endswith('.tif'):
                folder = os.path.join(root)
                folder = folder.replace('\\','/')
                if folder not in tiffFolders:
                    tiffFolders.append(folder)
    for folder in tiffFolders:
        parentFolder = '/'.join(folder.split('/')[:-1])
        tiffsList = []
        pdfName = folder.split('/')[-1]
        genericTest = re.match('tiffs|tiff|master|masters',pdfName.lower())
        if genericTest:
            pdfName = folder.split('/')[-2]
        pdfPath = os.path.join(parentFolder,pdfName + '.pdf')
        fileList = os.listdir(folder)
        for file in fileList:
            if file.lower().endswith('.tif'):
                tiffsList.append(os.path.join(folder,file))
        tiffsList.sort()
        print('Creating PDF from folder: ' + folder)
        imageList = []
        for tiff in tiffsList:
            imageList.append(Image.open(tiff))
        imageList[0].save(pdfPath, save_all=True, append_images=imageList[1:])
