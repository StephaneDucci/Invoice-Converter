## Main Foreign Supplier Invoice Converter

This Python script, hosted in a Colab notebook within the company cloud, allows users to upload a PDF invoice from the supplier Anker and outputs an Excel file containing exclusive product data along with all relevant details:
- SKU
- Description
- Quantity
- Alcohol Volume (%)
- Bottles per Case (bt/cs)
- Bottle Price
- Total Price

The script uses the following libraries:
- **Tesseract**: An OCR (Optical Character Recognition) tool that extracts text from images, allowing the extraction of text from PDF invoices.
- **pdf2image**: Converts pages of the PDF into images, which can then be processed by Tesseract to extract text.
- **Pandas**: Structures the extracted data into a DataFrame for easy manipulation and conversion into Excel format.
- **re**: Uses regular expressions to recognize and extract key pieces of information from the extracted text accurately.

This automation allows for a more efficient way to verify invoices and perform quick analyses of the products purchased.

### Notebooks and Scripts

- **AnkerProformaConverter.ipynb**: A Colab notebook that runs the script in the cloud.
  
- **AnkerProformaConverter.py**: A Python script executable on a local machine with Python installed. The script requires modification to correct:
  - The path to Poppler
  - The path to Tesseract
  - The temporary path where images are saved for text recognition
  - The paths of the three outputs:
    - The CSV output file
    - Two TXT files for errors and lines intentionally not exported
