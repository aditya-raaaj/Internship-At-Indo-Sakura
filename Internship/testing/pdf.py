import fitz
import pdfplumber

a = r"C:\Users\DELL\Downloads\Leveraging_AI_Technology_for_Coding_the_Classroom_Observation_Record_Form_of_Flanders_Interaction_Analysis.pdf"
doc = fitz.open(a)
page = doc[6]
txt = page.get_text()
print(txt)
for page_num in range(len(doc)):
    for img in doc[page_num].get_images():
        xref = img[0]  # Image reference number
        base_image = doc.extract_image(xref)  # Extract image
        image_bytes = base_image["image"]

        with open(f"image_{page_num + 1}_{xref}.png", "wb") as img_file:
            img_file.write(image_bytes)

with pdfplumber.open(a) as pdf:
    page = pdf.pages[8]  # Extract tables from the 7th page (index starts at 0)
    tables = page.extract_tables()

    for table_num, table in enumerate(tables, start=1):
        print(f"Table {table_num}:")
        
        headers = table[0]  # Assuming first row contains headers
        data_rows = table[1:]  # Remaining rows
        
        print("Headers:", headers)
        print("Data:")
        for row in data_rows:
            print(row)
        print("\n" + "-"*40 + "\n")

doc.close()
