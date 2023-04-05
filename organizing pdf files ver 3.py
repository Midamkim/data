import os
import PyPDF2
import pytesseract
import ocrmypdf
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine, LTAnno
import math

poppler_path = "C:/Program Files/poppler-23.01.0/Library/bin"
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def ocr(file_path, save_path):
   ocrmypdf.ocr(file_path, save_path)

def extract_title(pdf_path):
    max_avg_font_size = -1
    title_lines = []

    for page_layout in extract_pages(pdf_path):
        print(f"pdf_path: {pdf_path}")
        lines = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if isinstance(text_line, LTTextLine):
                        line_text = ""
                        font_sizes_sum = 0
                        char_count = 0
                        is_italic = False

                        for character in text_line:
                            if isinstance(character, LTChar):
                                line_text += character.get_text()
                                font_sizes_sum += character.size
                                char_count += 1
                                # Check if the font name indicates italic style
                                if "Ital" in character.fontname:
                                    is_italic = True
                                upper = line_text.isupper()
                            if isinstance(character, LTAnno):
                                line_text += character.get_text()

                        if char_count > 0:
                            avg_font_size = math.ceil(font_sizes_sum / char_count)
                            print(avg_font_size)
                            if avg_font_size > max_avg_font_size:
                                max_avg_font_size = avg_font_size

                            lines.append((avg_font_size, is_italic, upper, line_text.strip(), text_line.y0))

        # Sort lines based on average font size and y0 value
        lines.sort(key=lambda x: (x[0], x[4]),reverse=True)

        #Extract lines with the largest font size to form the title
        for i in range(len(lines)):
            if lines[i][0] == max_avg_font_size:
                if lines[i][1] == False:
                    title_lines.append(lines[i][3])
                elif lines[i][1] == True:
                    if lines [i+1][2] == True:
                        title_lines.append(lines[i+1][3])
                    elif lines [i+1][2] == False:
                        title_lines.append(lines[i+2][3])
                else:
                    break
        # Stop after processing the first page
        break

    return "".join(title_lines)

folder_path = input("folder path: ")  # replace with the path to your folder

# loop through all the files in the folder
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
                title = extract_title(file_path).replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').replace('*', '').replace('â€™', '').replace('∗', '').replace(',', '').replace('+', '').strip()

                if title.split()[0] == "Journal":
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    title = pdf_reader.metadata.title.replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').replace('*', '').replace('â€™', '').replace('∗', '').replace(',', '').replace('+', '').strip()
            except IndexError:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                title = pdf_reader.metadata.title.replace(':', '_').replace('?', '_').replace('', '').replace('/','_').replace('.', '').replace('', '').replace('*', '').replace('â€™', '').replace('∗', '').replace(',', '').replace('+', '').strip()

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
