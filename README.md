# images_to_pdf
Combine all images of a given format in a directory into a single multi-page PDF, or run recursively to create one PDF per subdirectory of images

This script combines a directory (or several directories) of images to a single PDF. Because this script uses JPEG compression to reduce the size of the PDF file output, the resulting PDFs may or may not be considered suitable for publishing.

To install the required Pillow library:
    
    <code>python -m pip install --upgrade pip</code>

    <code>python -m pip install Pillow</code>

Provide the path to an input directory containing images, or run without providing a directory to run the script on the current working directory:

    <code>python images_to_pdf.py <path_to_directory></code>
	
By default, the script searches for and combines TIFF images to PDF, but it can also search for JPEG or PNG images. Use the <code>-f --format</code> switch followed by one of these extensions to combine images of that format, rather than TIFFs, into a PDF:
	
	<code>python images_to_pdf.py <path_to_directory> -f png</code>
	
The script will only search for one file format at a time to create PDFs. If a directory contains images of multiple formats, only images of the specified format (or TIFFs by default) will be compiled into a PDF when the script is run.
    
To run the script recursively (i.e. including any subdirectories containing images), use the <code>-r --recursive</code> switch:

    <code>python images_to_pdf.py <path_to_root_folder> -r</code>
    
When run recursively, the script will identify any folders containing image files and create a PDF one directory above the images themselves. The PDF file will be named according to the folder containing the images. If that folder is named after a file format (e.g. "TIFFs", "JPG") or a file tier (e.g. "Masters", "Derivative"), the PDF will be given the name of that folder's parent folder, in an attempt to capture a better object name for the PDF. Additional "generic" folder names to be ignored can be added to the "genericTest" list on line <code>133</code>.

To specify a custom PDF output directory, use the <code>-o --output</code> switch and provide the path to a directory:

	<code>python images_to_pdf.py <path_to_directory> -o <path_to_output_directory></code>
	
An OCR text layer can be applied to the output PDF file(s) using the <code>-t --tesseract</code> switch:
	
	<code>python images_to_pdf.py <path_to_directory> -t</code>

The tesseract switch requires that pytesseract be installed in your working environment. In Windows, Tesseract must be installed and mapped to the <code>PATH</code> system environment variable.

All switches can be used in combination with one another.

