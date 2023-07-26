import os
import re
import io
import argparse
import sys
from PIL import Image, ImageSequence, PdfParser
from PyPDF2 import PdfFileWriter, PdfFileReader

parser = argparse.ArgumentParser(description='Compile all images of a given format in a directory into a single PDF. '
                                 'If no image directory is provided, the script will run in the current working directory. '
                                 'If no image format is provided, the script will search for TIFFs by default. '
                                 'Optionally, run recursively on all subdirectories. '
                                 'Optionally, specify an output directory for PDF files other than the directory containing images themselves. '
                                 'Optionally, OCR the created PDF files to allow them to be searched. ')

parser.add_argument('directory', help="directory containing tiffs to be converted to pdf", action="store", nargs='?', default=os.getcwd())
parser.add_argument('-r', '--recursive', help="recursively create pdfs in all subdirectories containing tiffs", action="store_true", dest="r", required=False)
parser.add_argument('-o', '--output', help="specify an output directory for all created PDFs", action="store", dest="o", required=False)
parser.add_argument('-t', '--tesseract', help="apply an OCR text layer using Tesseract", action="store_true", dest="t", required=False)
parser.add_argument('-f', '--format', help="specify an image file format to compile into a PDF, instead of TIFF", action="store", dest="f", default='tif', required=False)

args = parser.parse_args()

if args.t:
    import pytesseract

pageNum = 0

inputFormat = args.f
inputFormat = inputFormat.lower()
if inputFormat == 'jpeg':
    inputFormat = 'jpg'
if inputFormat == 'tiff':
    inputFormat = 'tif'
if inputFormat != 'jpg':
    if inputFormat != 'tif':
        if inputFormat != 'png':
            sys.exit('Invalid input format specified. Accepted file formats are TIFF, JPEG, and PNG')

# Append TIFFs to an existing PDF, or create a new PDF if needed.
# Use pageNum to determine if a new PDF needs to be created, in case a PDF
# is already in place and needs to be overwritten.
# Iterate over TIFFs to include all frames of multi-page TIFFs.
# Convert black and white TIFFs to grayscale and remove RGBA alpha layer

def converter(imageList, pdfPath):
    global pageNum
    pdf_pages = []
    try:
        print('Creating PDF: ' + pdfPath + '\n')
        for imageFile in imageList:
            img = Image.open(imageFile)
            if args.t:
                pdf = pytesseract.image_to_pdf_or_hocr(img, lang='eng', extension='pdf') #add a condition where this is only used if the ocr option is enabled
                pdf_pages.append(pdf)
                pdf_writer = PdfFileWriter()
                for page in pdf_pages:
                    pdf = PdfFileReader(io.BytesIO(page))
                    pdf_writer.addPage(pdf.getPage(0))
                file = open(pdfPath, "w+b")
                pdf_writer.write(file)
                file.close()
            else:
                for frame in ImageSequence.Iterator(img):
                    if img.mode == '1':
                        frame = frame.convert('L')
                    if img.mode == 'RGBA':
                        frame = frame.convert('RGB')
                    try:
                        if pageNum == 0:
                            frame.save(pdfPath)
                            #print('Creating PDF: ' + pdfPath + '\n')
                        else:
                            frame.save(pdfPath, append=True)
                    except PdfParser.PdfFormatError:
                        print('Error: Existing PDF fragment found at ' + pdfPath + ', possibly because this script was previously run and interrupted. Try deleting the fragment and running tiffs_to_pdf again')
                    pageNum += 1
    except IndexError:
        print('Error: \"' + args.directory + '\" contains no images of the specified format\n')


# If the recursive option wasn't passed, create the list of TIFFs in the named
# folder (or in the current working directory) and create the PDF in place there
if not args.r:
    imagesList = []
    folderPath = args.directory
    folderPath = folderPath.replace('\\', '/')
    folderName = folderPath.split('/')[-1]
    pdfName = folderName + '.pdf'
    if args.o:
        pdfPath = os.path.join(args.o, pdfName)
    else:
        pdfPath = os.path.join(folderPath, pdfName)
    pdfPath = pdfPath.replace('\\', '/')
    if os.path.exists(pdfPath):
        suffix = 1
        newPdfPath = pdfPath[:-4] + '_' + str(suffix) + '.pdf'
        while os.path.exists(newPdfPath):
            suffix += 1
            newPdfPath = pdfPath[:-4] + '_' + str(suffix) + '.pdf'
        print('CHANGING OUTPUT: ' + pdfPath + ' already exists. PDF will be named ' + newPdfPath[:-4] + '.pdf')
        pdfPath = newPdfPath
    fileList = os.listdir(folderPath)
    pageNum = 0
    for file in fileList:
        if file.lower().endswith(inputFormat):
            imagesList.append(os.path.join(folderPath, file))
    imagesList.sort()
    if len(imagesList) == 0:
        sys.exit('No ' + inputFormat + ' images found in folderPath. Choose another folder or use -r to run recursively')
    converter(imagesList, pdfPath)    
       
# If the recursive option was passed, find folders containing TIFFs. For each
# such folder, assemble TIFFs into a PDF. If the folder has a generic name,
# attempt to use a better PDF file name by looking one level higher
elif args.r:
    rootFolder = args.directory
    rootFolder = rootFolder.replace('\\','/')
    print('Searching recursively for ' + inputFormat + 's within ' + rootFolder + '\n')
    imagesFolders = []
    for root, dirs, files in os.walk(rootFolder):
        for file in files:
            if file.lower().endswith(inputFormat):
                folder = os.path.join(root)
                folder = folder.replace('\\','/')
                if folder not in imagesFolders:
                    imagesFolders.append(folder)

    for folder in imagesFolders:
        print(inputFormat + 's found in ' + folder)
        imagesList = []
        pdfName = folder.split('/')[-1] + '.pdf'
        genericTest = re.match('tiffs|tiff|tif|tifs|jpegs|jpeg|jpg|jpgs|png|pngs|master|masters|derivative|derivatives', pdfName.lower())
        if genericTest:
            folderName = folder.split('/')[-1]
            pdfName = folder.split('/')[-2] + '.pdf'
            print('CHANGING OUTPUT: "' + folderName + '" is a generic folder name. Using parent folder name. PDF will be named "' + pdfName + '"')
        if args.o:
            pdfPath = os.path.join(args.o, pdfName)
        else:
            pdfPath = os.path.join(folder, pdfName)
        pdfPath = pdfPath.replace('\\', '/')
        if os.path.exists(pdfPath):
            suffix = 1
            newPdfPath = pdfPath[:-4] + '_' + str(suffix) + '.pdf'
            while os.path.exists(newPdfPath):
                suffix += 1
                newPdfPath = pdfPath[:-4] + '_' + str(suffix) + '.pdf'
            print('CHANGING OUTPUT: ' + pdfPath + ' already exists. PDF will be named ' + newPdfPath[:-4] + '.pdf')
            pdfPath = newPdfPath
            
        fileList = os.listdir(folder)
        pageNum = 0
        for file in fileList:
            if file.lower().endswith(inputFormat):
                imagesList.append(os.path.join(folder,file))
        imagesList.sort()
        converter(imagesList, pdfPath)
