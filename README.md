# PDF Combiner Tool Improvements

Updated Description:
 
 # Version 3.0

- Class-based Structure: The code is now encapsulated in a PDFCombinerApp class, which improves organization and reusability.
Scrollbar: Added a scrollbar to the listbox for better file management.

- Progress Bar: Introduced a progress bar to provide visual feedback during the PDF combining process.

- Blinking Effect: Improved the blinking effect using after method instead of an infinite loop.

- Threading: Utilized threading to prevent the GUI from freezing during the PDF combining process.

## Requirements

- Python 3
- PyPDF2
- fpdf

## Installation

pip install PyPDF2 fpdf

git clone https://github.com/ADITYANAIR01/PDFCombiner.git

cd PDFCombiner

python pdf_combiner.py
