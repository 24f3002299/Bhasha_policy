import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path: str) -> list[Document]:
    """
    Extracts text from a PDF, falling back to OCR if the document appears to be scanned.
    Returns a list of LangChain Document objects.
    """
    print(f"Starting extraction for: {pdf_path}")
    
    # STEP 1: Try normal PDF extraction first
    loader = PyPDFLoader(pdf_path)
    pdf_docs = loader.load()

    extracted_text = ""
    for doc in pdf_docs:
        extracted_text += doc.page_content

    print(f"Characters extracted normally: {len(extracted_text)}")

    # STEP 2: Decide whether OCR is needed
    if len(extracted_text.strip()) < 1000:
        print("⚠️ Scanned PDF detected. Running OCR...")
        pages = convert_from_path(pdf_path, 300)
        documents = []
        
        for page_num, page in enumerate(pages, start=1):
            text = pytesseract.image_to_string(page, config="--psm 6")
            documents.append(
                Document(
                    page_content=text,
                    metadata={"page": page_num}
                )
            )
    else:
        print("✅ Text-based PDF detected. OCR skipped.")
        documents = []
        
        for page_num, doc in enumerate(pdf_docs, start=1):
            documents.append(
                Document(
                    page_content=doc.page_content,
                    metadata={"page": page_num}
                )
            )

    return documents