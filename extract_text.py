# -*- coding: utf-8 -*-
import re
import fitz
import os

#---------------------------------------
# Document directory PATHS
#---------------------------------------
DIR_PATH  = '/content/drive/MyDrive/MSA/'
PDF_PATH  = DIR_PATH+'PDF/'
DOC_PATH  = DIR_PATH+'DOC/'
JSON_PATH = DIR_PATH + 'JSON_PDF/' 
DOC_TXT_PATH = DIR_PATH + 'JSON_DOC/'


def convert_pdf_to_txt(pdf_file):
        doc = fitz.open(pdf_file)
        raw_text= ""

        for page in doc:
            raw_text = raw_text + page.get_text() + "\n"

        try:
            full_string = re.sub(r'\n+', '\n', raw_text)
            full_string = full_string.replace("\r", "\n")
            full_string = full_string.replace("\t", " ")

            # Remove awkward LaTeX bullet characters
            full_string = re.sub(r"\uf0b7", " ", full_string)
            full_string = re.sub(r"\(cid:\d{0,3}\)", " ", full_string)
            full_string = re.sub(r'• ', " ", full_string)

            # Split text blob into individual lines
            lines = full_string.splitlines(True)

            # Remove empty strings and whitespaces
            clean_lines = [re.sub('\s+', ' ', line.strip()) for line in lines if line.strip()]

            return clean_lines
        except Exception as e:
            print('Error in PDF file:: ' + str(e))
            return []

def convert_docx_to_txt(docx_file,docx_parser):
      doc = docx.Document(docx_file)
      allText = []
      for docpara in doc.paragraphs:
          allText.append(docpara.text)
      text = '\n'.join(allText)
      try:
          clean_text = re.sub(r'\n+', '\n', text)
          clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
          lines = clean_text.splitlines(True)  # Split text blob into individual lines
          clean_lines = [re.sub('\s+', ' ', line.strip()) for line in lines if
                          line.strip()]  # Remove empty strings and whitespaces
          print (f'{len(clean_lines)} - Number of lines.')
          return clean_lines
      except Exception as e:
          print('Error in docx file:: ' + str(e))
          return []



def list_files(directory,file_ext):
    files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(file_ext):
            files.append(file_name)
    return files

pdf_files = list_files(PDF_PATH,".pdf")

# Print the PDF files
for pdf_file in pdf_files:
    print(pdf_file)
    json_file =  normal_file = os.path.splitext(pdf_file)[0] + ".json"
    txt_file  =  normal_file = os.path.splitext(pdf_file)[0] + ".txt"

    lines = convert_pdf_to_txt(PDF_PATH+pdf_file)
    json_data = extract_headings_and_paragraphs(lines)
    with open(JSON_PATH+txt_file, "w") as file:
      file.write("\n".join(lines))
    break

doc_files = list_files(DOC_PATH,".docx")

# Print the DOC files
for file in doc_files:
    print(file)
    json_file =  normal_file = os.path.splitext(file)[0] + ".json"
    txt_file  =  normal_file = os.path.splitext(file)[0] + ".txt"
    docx_parser = "tika"
    lines = convert_docx_to_txt(DOC_PATH+file,docx_parser)
    json_data = extract_headings_and_paragraphs(lines)
    with open(DOC_TXT_PATH+txt_file, "w") as file:
      file.write("\n".join(lines))
    break

