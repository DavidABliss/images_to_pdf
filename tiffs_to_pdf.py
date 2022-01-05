import os
import re
from PIL import Image,ImageSequence
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('directory', help="directory containing tiffs to be converted to pdf", action="store", nargs='?', default=os.getcwd())
parser.add_argument('-r', '--recursive', help="recursively create pdfs in all subdirectories containing tiffs", action="store_true", dest="r", required=False)

args = parser.parse_args()

if not args.r:
    tiffsList = []
    folderPath = args.directory
    folderPath = folderPath.replace('\\', '/')
    folderName = folderPath.split('/')[-1]
    pdfPath = folderPath + '/' + folderName + '.pdf'
    fileList = os.listdir(folderPath)
    for file in fileList:
        if file.lower().endswith('.tif'):
            tiffsList.append(folderPath + '/' + file)
    tiffsList.sort()
    imageList = []
    try:
        for tiff in tiffsList:
            img = Image.open(tiff)
            for frame in ImageSequence.Iterator(img):
                if img.mode == '1':
                    frame = frame.convert('L')
                if img.mode == 'RGBA':
                    frame = frame.convert('RGB')
                if not os.path.exists(pdfPath):
                    frame.save(pdfPath)
                elif os.path.exists(pdfPath):
                    frame.save(pdfPath, append=True)
    except IndexError:
        print('Error: \"' + args.directory + '\" contains no TIFFs')        

elif args.r:
    rootFolder = args.directory
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
            img = Image.open(tiff)
            for frame in ImageSequence.Iterator(img):
                if img.mode == '1':
                    frame = frame.convert('L')
                if img.mode == 'RGBA':
                    frame = frame.convert('RGB')
                if not os.path.exists(pdfPath):
                    frame.save(pdfPath)
                elif os.path.exists(pdfPath):
                    frame.save(pdfPath, append=True)
