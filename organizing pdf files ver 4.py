import os
import PyPDF2
import pytesseract
import ocrmypdf
import spacy
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine
import math

poppler_path = "C:/Program Files/poppler-23.01.0/Library/bin"
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Load pre-trained NLP models from spaCy
ennlp = spacy.load("en_core_web_lg")

def ocr(file_path, save_path):
   ocrmypdf.ocr(file_path, save_path)

def extract_title(pdf_path):
    max_font_size = -1
    title_lines = []

    for page_layout in extract_pages(pdf_path):
        lines = []

        is_bold = False
        break_outer_loop = False

        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:

                    if isinstance(text_line, LTTextLine):
                        line_text = text_line.get_text()

                        endoc = ennlp(line_text)
                        enauthors = {ent.text for ent in endoc.ents if ent.label_ == 'PERSON'}
                        if enauthors != set() :
                            print(f"authors: {enauthors}")
                            break_outer_loop = True
                            break

                        first_char = next((text_obj for text_obj in text_line if isinstance(text_obj, LTChar)), None)
                        first_letter = first_char.get_text()
                        font_size = math.ceil(first_char.size)
                        font_name = first_char.fontname
                        if font_name.find("Bold") > -1:
                            is_bold = True
                        upper = first_letter.isupper()

                        if font_size >= max_font_size:
                            max_font_size = font_size
                            lines.append((font_size, is_bold, upper, line_text.strip(), text_line.y0))

                if break_outer_loop:
                    break

        # Sort lines based on average font size and y0 value
        lines.sort(key=lambda x: (x[0], x[4]),reverse=True)

        #Extract lines with the largest font size to form the title
        for i in range(len(lines)):
            if lines[i][0] == max_font_size:
                title_lines.append(lines[i][3])
            else:
                break
        break

    return " ".join(title_lines)

folder_path = input("folder path: ")  # replace with the path to your folder
ocrrequest = input("OCR, too, y or n?")

# loop through all the files in the folder
if ocrrequest == "y":
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as pdf_file:
                # read the PDF file and OCR it if it is not readable
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                try:
                    title = pdf_reader.pages[0].extract_text().split('\n')[0]
                    print(title)
                    if title.split()[0] == "Submitted":
                        print("okay")
                    else:
                        print("okay")
                except IndexError:
                    print(f"I'm OCRing {file_name}.")
                    print(file_path)
                    ocr(file_path,file_path)
                    print("OCR done")

for file_name in os.listdir(folder_path):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rb') as pdf_file:

            try:
                title = extract_title(file_path).replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').replace('*', '').replace('â€™', '').replace('∗', '').replace(',', '').replace('+', '').replace('\n','_').replace('"', '').strip()

                if title.split()[0] == "Journal":
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    title = pdf_reader.metadata.title.replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').replace('*', '').replace('â€™', '').replace('∗', '').replace(',', '').replace('+', '').replace('\n','_').replace('"', '').strip()
            except IndexError:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                title = pdf_reader.metadata.title.replace(':', '_').replace('?', '_').replace('', '').replace('/','_').replace('.', '').replace('', '').replace('*', '').replace('â€™', '').replace('∗', '').replace(',', '').replace('+', '').replace('\n','_').replace('"', '').strip()

    # rename the file with the title of the research paper
    new_file_name = f'{title}.pdf'
    print(f"NEW title: {new_file_name}")
    new_file_path = os.path.join(folder_path, new_file_name)
    pdf_file.close()

    try:
        os.rename(file_path, new_file_path)
    except FileExistsError:
        title = f"{title}_new"
        new_file_name = f'{title}.pdf'
        print(f"new title: {new_file_name}")
        new_file_path = os.path.join(folder_path, new_file_name)
        pdf_file.close()
        os.rename(file_path, new_file_path)
