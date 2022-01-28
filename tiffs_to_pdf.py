import os
import sys
import re
from PIL import Image,ImageSequence,PdfParser
import argparse

parser = argparse.ArgumentParser(description='Compile all TIFFs in a directory into a single PDF. '
                                 'If no TIFF directory is provided, the script will run in the current working directory. '
                                 'Optionally, run recursively on all subdirectories. ')

parser.add_argument('directory', help="directory containing tiffs to be converted to pdf", action="store", nargs='?', default=os.getcwd())
parser.add_argument('-r', '--recursive', help="recursively create pdfs in all subdirectories containing tiffs", action="store_true", dest="r", required=False)
parser.add_argument('-o', '--output', help="specify an output directory for all created PDFs", action="store", dest="o", required=False)

args = parser.parse_args()

pageNum = 0


# Append TIFFs to an existing PDF, or create a new PDF if needed.
# Use pageNum to determine if a new PDF needs to be created, in case a PDF
# is already in place and needs to be overwritten.
# Iterate over TIFFs to include all frames of multi-page TIFFs.
# Convert black and white TIFFs to grayscale and remove RGBA alpha layer
def converter(imageList, pdfPath):
    global pageNum
    try:
        for tiff in imageList:
            img = Image.open(tiff)
            for frame in ImageSequence.Iterator(img):
                if img.mode == '1':
                    frame = frame.convert('L')
                if img.mode == 'RGBA':
                    frame = frame.convert('RGB')
                try:
                    if pageNum == 0:
                        frame.save(pdfPath)
                        print('Creating PDF: ' + pdfPath + '\n')
                    else:
                        frame.save(pdfPath, append=True)
                except PdfParser.PdfFormatError:
                    print('Error: Existing PDF fragment found at ' + pdfPath + '. Try deleting the fragment and running tiffs_to_pdf again')
                pageNum += 1
    except IndexError:
        print('Error: \"' + args.directory + '\" contains no TIFFs\n')
    

# If the recursive option wasn't passed, create the list of TIFFs in the named
# folder (or in the current working directory) and create the PDF in place there
if not args.r:
    tiffsList = []
    folderPath = args.directory
    folderPath = folderPath.replace('\\', '/')
    folderName = folderPath.split('/')[-1]
    pdfName = folderName + '.pdf'
    if args.o:
        pdfPath = os.path.join(args.o, pdfName)
    else:
        pdfPath = os.path.join(folderPath, pdfName)
    pdfPath = pdfPath.replace('\\', '/')
    fileList = os.listdir(folderPath)
    pageNum = 0
    for file in fileList:
        if file.lower().endswith('.tif'):
            tiffsList.append(os.path.join(folderPath, file))
    tiffsList.sort()
    if len(tiffsList) == 0:
        sys.exit('No TIFFs found in folderPath. Choose another folder or use -r to run recursively')
    converter(tiffsList, pdfPath)    
       
# If the recursive option was passed, find folders containing TIFFs. For each
# such folder, assemble TIFFs into a PDF. If the folder has a generic name,
# attempt to use a better PDF file name by looking one level higher
elif args.r:
    rootFolder = args.directory
    rootFolder = rootFolder.replace('\\','/')
    print('Searching recursively for TIFFs within ' + rootFolder + '\n')
    tiffFolders = []
    for root, dirs, files in os.walk(rootFolder):
        for file in files:
            if file.lower().endswith('.tif'):
                folder = os.path.join(root)
                folder = folder.replace('\\','/')
                if folder not in tiffFolders:
                    tiffFolders.append(folder)

    for folder in tiffFolders:
        print('TIFFs found in ' + folder)
        tiffsList = []
        pdfName = folder.split('/')[-1] + '.pdf'
        genericTest = re.match('tiffs|tiff|master|masters', pdfName.lower())
        if genericTest:
            folderName = folder.split('/')[-1]
            pdfName = folder.split('/')[-2] + '.pdf'
            print('"' + folderName + '" is a generic folder name. PDF will be named "' + pdfName)
        if args.o:
            pdfPath = os.path.join(args.o, pdfName)
        else:
            pdfPath = os.path.join(folder, pdfName)
        pdfPath = pdfPath.replace('\\', '/')
        fileList = os.listdir(folder)
        pageNum = 0
        for file in fileList:
            if file.lower().endswith('.tif'):
                tiffsList.append(os.path.join(folder,file))
        tiffsList.sort()
        converter(tiffsList, pdfPath)
