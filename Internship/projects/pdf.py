import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import numpy as np
import cv2
import tempfile

# Configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESS_LANG = 'eng+jpn'
DEBUG_MODE = True  # Set to True to display edge + Hough overlays

# Preprocess image for OCR
def preprocess_image(img_np):
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 15, 11
    )
    return processed

# Check orientation using Canny + Hough
def is_vertical_text(img_np):
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=200)

    if lines is None:
        return False

    vertical_lines = []
    for rho, theta in lines[:, 0]:
        angle = theta * 180 / np.pi
        if 80 <= angle <= 100:
            vertical_lines.append((rho, theta))

    if DEBUG_MODE:
        edge_display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        for rho, theta in vertical_lines:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(edge_display, (x1, y1), (x2, y2), (0, 0, 255), 2)
        st.image(edge_display, caption="🕵️ Detected Vertical Lines", use_column_width=True)

    return len(vertical_lines) > 5

# Convert PDF page to image (2x zoom)
def pdf_page_to_image(page):
    mat = fitz.Matrix(2, 2)  # Higher DPI
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

# Extract text with rotation handling and preprocessing
def extract_text(pil_img):
    img_np = np.array(pil_img)
    if is_vertical_text(img_np):
        img_np = cv2.rotate(img_np, cv2.ROTATE_90_CLOCKWISE)

    preprocessed = preprocess_image(img_np)
    return pytesseract.image_to_string(preprocessed, lang=TESS_LANG, config="--psm 5")

# Streamlit App
def main():
    st.set_page_config(page_title="High-Precision OCR (ENG+JPN)", layout="centered")
    st.title("📄 OCR with Vertical Detection + Preprocessing")

    uploaded_file = st.file_uploader("Upload a scanned PDF", type="pdf")

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.read())
            pdf_path = temp_pdf.name

        doc = fitz.open(pdf_path)
        st.success(f"Loaded {len(doc)} pages.")

        all_text = ""
        for i, page in enumerate(doc):
            st.write(f"---\n### 📃 Page {i + 1}")
            pil_img = pdf_page_to_image(page)
            st.image(pil_img, caption=f"Rendered Page {i + 1}", use_column_width=True)

            text = extract_text(pil_img)
            st.text_area("📝 OCR Output", text, height=200)
            all_text += f"--- Page {i + 1} ---\n{text}\n"

        st.download_button("📥 Download All Text", all_text, file_name="ocr_output.txt")

if __name__ == "__main__":
    main()
