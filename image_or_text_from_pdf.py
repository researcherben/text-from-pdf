#!/usr/bin/env python
# coding: utf-8

# used by pdf2image
!conda install -c conda-forge poppler --yes
!conda install -c conda-forge tesseract --yes')

# # PDFminer
# https://pypi.org/project/pdfminer/
# https://github.com/pdfminer/pdfminer.six
!pip install pdfminer.six

# used by pdf2image
!pip3 install Pillow # https://pypi.org/project/Pillow/
!pip install PyPDF2
!pip3 install pdf2image
!pip3 install pytesseract

# https://pypi.org/project/pdf2image/
# https://pdf2image.readthedocs.io/en/latest/reference.html

# depends on poppler being installed
from pdf2image import convert_from_path

import pytesseract
import time
import glob
# # PyPDF2
# https://pypi.org/project/py2pdf/
import PyPDF2


all_pdfs = glob.glob("docxs/*.pdf")
all_data = {}

for pdf_filename in all_pdfs:
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



for pdf_filename in all_pdfs:
    #print("=====",pdf_filename,"=====")
    !pdf2txt.py "$pdf_filename" > file_text.txt
    with open('file_text.txt','r') as file_handle:
        file_content = file_handle.read()
    all_data[pdf_filename]['pdfminer'] = file_content


# PDF to image to text (using tesseract)

start_time = time.time()
for pdf_filename in all_pdfs:
    print(pdf_filename)
    pages = convert_from_path(pdf_filename, dpi=350)

    i = 1
    all_pages = ""
    for page in pages:
        print("page",i,round(time.time()-start_time,2),'seconds')
        image_name = pdf_filename + "_" + str(i) + ".jpg"  
        page.save(image_name, "JPEG")
        
        page_content = pytesseract.image_to_string(image_name, lang='eng')
        all_pages += page_content.lower().replace('.','')
    all_data[pdf_filename]['tesseract'] = all_pages


group_keywords = {"group 1": ["word1","word2"], # OR within that list
                  "group 2": ["word2", "corporation"], 
                  "group 3": ["bob"]}

list_of_words = []
for group, word_list in group_keywords.items():
    for word in word_list:
        list_of_words.append(word)

list_of_word_stems = list(set(list_of_words))


# print all the content
for filename, content_dict in all_data.items():
    print(filename)
    for libraryname, content_str in content_dict.items():
        print("  ", libraryname)
        cleaned_str = content_str.lower().replace('.','')
        print(cleaned_str)
# show the matches per python library
for filename, content_dict in all_data.items():
    print(filename)
    for libraryname, content_str in content_dict.items():
        print("  ", libraryname)
        cleaned_str = content_str.lower().replace('.','')
        for this_word in list_of_word_stems:
            if this_word in cleaned_str: print("     MATCH:", this_word)


for filename, content_dict in all_data.items():
    #print(filename)
    list_of_matched_words = []
    for libraryname, content_str in content_dict.items():
        cleaned_str = content_str.lower().replace('.','')
        for this_word in list_of_word_stems:
            if this_word in cleaned_str: 
                list_of_matched_words.append(this_word)
    uniq_matches = list(set(list_of_matched_words))
    if len(uniq_matches)==0:
        print(len(uniq_matches),'keyword matches in',filename,'\n')
    else: # at least one match
        str_to_print = str(len(uniq_matches)) + ' keyword matches in ' + filename +': '
        for matched_word in uniq_matches:
            str_to_print += matched_word + ", "
        print(str_to_print)
        
        groups_to_alert = []
        for group, word_list in group_keywords.items():
            for word in word_list:
                if word in uniq_matches:
                    groups_to_alert.append(group)
        str_to_print = "alert "
        for group in list(set(groups_to_alert)):
            str_to_print += group + " and "
        print(str_to_print[:-4]+"\n")

