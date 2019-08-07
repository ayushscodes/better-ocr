# -*- coding: utf-8 -*-
import docx
import subprocess
from tess_trainer import pdf_2_tif
import os
from sets import Set
from accuracy import accuracy_levenshtein
import sys
from fade_text.fade import apply_fade

"""
Calculates the accuracy on a set of documents for a new language that has been trained with tesseract training
"""

def getText(docx_file):
    doc = docx.Document(docx_file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def ocr_pdf(pdf_file, lang_name, im_aug):
    "Runs tesseract ocr on a pdf file using the specified language and returns th text generate"
    temp_out = 'tess_output'
    tif_file = pdf_2_tif(pdf_file)
    if im_aug:
        im_aug(tif_file, tif_file)
    command = ' '.join(['tesseract', tif_file, temp_out, '-l', lang_name])
    print(command)
    subprocess.Popen(command, shell=True).wait()
    text = open(temp_out + '.txt', 'r').read()

    return text

def docx_pdf_dir_accuracy(parent_dir, lang_name, output_file, im_aug=apply_fade):
    f = open(output_file, 'w')
    elements = Set(os.listdir(parent_dir))

    for element in os.listdir(parent_dir):
        docx_version = os.path.join(parent_dir, element)
        pdf_version = os.path.join(parent_dir, element[:-5]+'.pdf')
        print('docx versions is ', docx_version)
        print('pdf version is ', pdf_version)
        if '.docx' in element and element[:-5]+'.pdf' in elements:
            docx_text = getText(docx_version)
            print('docx text is of type ', type(docx_text))
            ocr_text = unicode(ocr_pdf(pdf_version, lang_name, im_aug), 'utf-8')
            print('ocr text is of type ', type(ocr_text))


            open(os.path.join(parent_dir, 'docx_text.txt'), 'w').write(docx_text.encode('utf-8'))
            open(os.path.join(parent_dir, 'ocr_text.txt'), 'w').write(ocr_text.encode('utf-8'))

            dist = accuracy_levenshtein(docx_text, ocr_text)
            output_string = ' '.join([str(dist), element[-5:], '\n'])
            print('accuracy is ', dist)
            f.write(output_string)
    f.close()
    return True


if __name__ == "__main__":
    output_file='acc_metrics.txt'
    parent_dir = sys.argv[1]
    lang_name = 'eng'
    docx_pdf_dir_accuracy(parent_dir, lang_name, output_file)
    print('Im done')



