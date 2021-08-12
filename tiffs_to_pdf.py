import sys
import os
import re
from PIL import Image

if not len(sys.argv) >= 2:
    print('Usage: python tiffs_to_pdf_uncompressed.py <path_to_folder>')
    sys.exit('To run recursively on several subdirectories: python tiffs_to_pdf_uncompressed.py <path_to_root_folder> -r')

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
