#!/usr/bin/env python
# coding: utf-8
# jupyter nbconvert --to script 'my-notebook.ipynb'

# https://github.com/umbcdata601/spring2020/tree/master/jupyter_notebooks/week_03_getting_data

!pip install pdfminer.six
!pip install PyPDF2

# # PDFminer
# https://pypi.org/project/pdfminer/
# https://github.com/pdfminer/pdfminer.six

list_of_word_stems = ['word1','word2','corporation']


import PyPDF2
import glob
all_files = glob.glob("docxs/*.pdf")
all_data = {}

for pdf_filename in all_files:
    #print("=====",pdf_filename,"=====")
    pdf_file = open(pdf_filename, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    #print(number_of_pages,'pages\n')
    content = ""
    for indx in range(number_of_pages):
        page = read_pdf.getPage(indx)
        page_content = page.extractText()
        #print(page_content.encode('utf-8'))
        content += str(page_content.encode('utf-8'))
    try:
        all_data[pdf_filename]['pypdf2'] = content
    except KeyError:
        all_data[pdf_filename] = {'pypdf2': content}


for pdf_filename in all_files:
    #print("=====",pdf_filename,"=====")
    !pdf2txt.py "$pdf_filename" > file_text.txt
    with open('file_text.txt','r') as file_handle:
        file_content = file_handle.read()
    all_data[pdf_filename]['pdfminer'] = file_content


for filename, content_dict in all_data.items():
    print(filename)
    for libraryname, content_str in content_dict.items():
        print("  ", libraryname)
        cleaned_str = content_str.lower().replace('.','')
        for this_word in list_of_word_stems:
            if this_word in cleaned_str: print("     MATCH:", this_word)
