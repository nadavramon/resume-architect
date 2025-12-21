import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text, or None if an error occurs.
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            # Iterate through all pages in the PDF
            for page in pdf.pages:
                # Extract text and add a newline character after each page
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# --- TEST BLOCK ---
# This block only runs when you execute this script directly.
if __name__ == "__main__":
    # 1. Ask user for a file name
    filename = input("Enter the name of your PDF file (e.g., resume.pdf): ")
    
    # 2. Run the extraction
    extracted_text = extract_text_from_pdf(filename)
    
    # 3. Print the result
    if extracted_text:
        print("\n--- EXTRACTED TEXT START ---")
        print(extracted_text)
        print("--- EXTRACTED TEXT END ---")
    else:
        print("No text found or error occurred.")