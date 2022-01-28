# tiffs_to_pdf
Convert TIFF images in a directory into a single multi-page PDF, or run recursively to create one PDF per subdirectory of TIFFs

This script converts a directory (or several directories) of TIFFs to a single PDF. It uses the Pillow PIL fork library to load and compress TIFFs before saving them as a single PDF. It is adapted from a previous version of the script that used ImageMagick for image handling, but Pillow handles these tasks much more quickly. Because Pillow uses JPEG compression to reduce the size of the PDF file output, the resulting PDFs may or may not be considered suitable for publishing.

To install the required Pillow library:
    
    python -m pip install --upgrade pip

    python -m pip install Pillow

Provide a custom directory argument, or run without providing a directory to run the script on the current working directory:

    python tiffs_to_pdf.py <path_to_directory>
    
To run the script recursively (i.e. including any subdirectories containing TIFFs), use the <code>-r --recursive</code> switch:

    python tiffs_to_pdf.py <path_to_root_folder> -r
    
When run recursively, the script will identify any folders containing TIFF files and create a PDF one directory above the TIFFs themselves. The PDF file will be named according to the folder containing the TIFFs. If that folder is named "TIFF", "TIFFs", "Master", or "Masters", the PDF will be given the name of that folder's parent folder, in an attempt to capture the object name for the PDF. Additional "generic" folder names to be ignored can be added to the "genericTest" list on line 91.

To specify a custom PDF output directory, use the <code>-r --output</code> switch and provide the path to a directory:

	python tiffs_to_pdf.py <path_to_directory> -o <path_to_output_directory>
	
The output switch can be used with or without the recursive switch.
