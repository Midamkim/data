import os
import PyPDF2
import pytesseract
import ocrmypdf

poppler_path = "C:/Program Files/poppler-23.01.0/Library/bin"
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def ocr(file_path, save_path):
   ocrmypdf.ocr(file_path, save_path)

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

             # read the PDF file and OCR it if it is not readable
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # extract the title of the research paper
            try:
                title = pdf_reader.metadata.title.replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').strip()
                if title.split()[0] == "Submitted":
                    title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').strip()
                elif title.split()[0] == "Published":
                    title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').strip()
                elif title.split()[0] == "IEEE":
                    title = pdf_reader.pages[0].extract_text().split('\n')[3].replace(':', '_').replace('?',  '_').replace('', '').replace('/', '_').replace('.', '').strip()
                elif title.split()[0][:5] == "ICPHS":
                    title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?',  '_').replace('', '').replace('/', '_').replace('.', '').strip()
                elif title.split()[0] == "Overleaf":
                    title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?',  '_').replace('', '').replace('/', '_').replace('.', '').strip()
                elif title.split()[0][:5] == "arXiv":
                    title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()

            except AttributeError:
                title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()
                print(title)
                if title.split()[0] == "Submitted":
                    title = pdf_reader.pages[0].extract_text().split('\n')[1].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()
                elif title.split()[0] == "Published":
                    title = pdf_reader.pages[0].extract_text().split('\n')[1].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()
                elif title.split()[0] == "IEEE":
                    title = pdf_reader.pages[0].extract_text().split('\n')[1].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()
                elif title.split()[0] == "r--,":
                    title = pdf_reader.pages[0].extract_text().split('\n')[3].replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()
                elif title.split()[0] == "1":
                    title = pdf_reader.pages[0].extract_text().split('\n')[1].replace(':', '_').replace('?', '_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()
                elif title.split()[0][:5] == "arXiv":
                    title = pdf_reader.pages[0].extract_text().split('\n')[0].replace(':', '_').replace('?','_').replace('', '').replace('/', '_').replace('.', '').replace('', '').strip()

    print(f"current title: {file_name}")
    firstfiveletters = title.split()[0][:5]
    print(firstfiveletters)

    # rename the file with the title of the research paper
    new_file_name = f'{title}.pdf'
    print(f"new title: {new_file_name}")
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
