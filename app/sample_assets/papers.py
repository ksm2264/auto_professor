import PyPDF4
import os

def extract_text_from_file(pdf_file, chunk_size=5000, overlap=200):
    """
    Extract text from a PDF file and split it into chunks with a specified size and overlap.

    Args:
        pdf_file (file): The file object of the opened PDF file.
        chunk_size (int, optional): The size of the text chunks. Defaults to 5000.
        overlap (int, optional): The number of overlapping characters between chunks. Defaults to 0.

    Returns:
        List[str]: A list of strings that are the text contents split into chunks with the specified size and overlap.
    """
    # Create a PDF reader object
    pdf_reader = PyPDF4.PdfFileReader(pdf_file)

    # Get the number of pages in the PDF file
    num_pages = pdf_reader.getNumPages()

    # Initialize an empty list to store the text chunks
    text_chunks = []

    # Loop through each page and extract the text
    for page in range(num_pages):
        page_obj = pdf_reader.getPage(page)
        text = page_obj.extractText()

        # Split the text into chunks with the specified size and overlap
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-overlap)]

        # Append the text chunks to the list
        text_chunks.extend(chunks)

    return text_chunks


def extract_text_from_path(pdf_path):
    """
    Extract text from a PDF file and split it into 5000 character chunks.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        List[str]: A list of strings that are the text contents split into 5000 character chunks.
    """
    # Open the PDF file in read binary mode
    with open(pdf_path, 'rb') as file:
        text_chunks = extract_text_from_file(file)

    return text_chunks


# Get the path to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the PDF file relative to the script's directory
pdf_path = os.path.join(script_dir, 'a_really_cool_paper.pdf')

# Extract the text from the PDF file
sample_text_chunks = extract_text_from_path(pdf_path)

if __name__ == '__main__':

    # Print the text chunks
    for chunk in sample_text_chunks:
        print(chunk)