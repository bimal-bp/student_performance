import streamlit as st
import pdfplumber
from PIL import Image
import requests
from io import BytesIO

# Function to fetch PDF from Google Drive (works in a web viewer)
def fetch_pdf_from_drive(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Function to display PDF pages as images in Streamlit
def display_pdf(pdf_url):
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            for page in pdf.pages:
                img = page.to_image().annotated  # Convert page to an image
                st.image(img, use_column_width=True)
    else:
        st.error("Failed to load PDF. Please check the link.")

# Streamlit App Layout
st.title("📄 PDF Viewer in Streamlit")

# Google Drive PDF file IDs
math_pdf_id = "1Os8nxl_EwyadsKhrAgagmjg3sHTH2Ylc"  # Replace with actual Math PDF ID
computer_pdf_id = "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp"  # Replace with actual Computer PDF ID

# Generate direct links
math_pdf_url = fetch_pdf_from_drive(math_pdf_id)
computer_pdf_url = fetch_pdf_from_drive(computer_pdf_id)

# Dropdown to select PDF
pdf_choice = st.selectbox("Select a PDF:", ["Math PDF", "Computer PDF"])

# Display the selected PDF
if pdf_choice == "Math PDF":
    display_pdf(math_pdf_url)
elif pdf_choice == "Computer PDF":
    display_pdf(computer_pdf_url)
