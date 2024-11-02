## Anker-Invoice-Converter

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

