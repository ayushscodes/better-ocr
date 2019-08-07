#!/usr/bin/python
# -*- coding: utf-8 -*-
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import os
import subprocess
import sys
from accuracy import accuracy
import csv
import json


def pdf_2_jpeg(input_filepath, im_prepro=False):
    if input_filepath[-4:] != '.pdf':
        raise ValueError("The input file must be a pdf")

    output_dir = input_filepath[:-4]
    print(output_dir)
    subprocess.Popen(['mkdir', output_dir]).wait()
    im_paths = []

    if im_prepro:
        for element in os.listdir(output_dir):
            if '.jpeg' in element:
                im_paths.append(os.path.join(output_dir, element))


    else:

        if "0.jpeg" in os.listdir(output_dir):
            return True

        image_pdf = Image(filename=input_filepath, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')

        counter = 0
        for img in image_jpeg.sequence:
            im_path = os.path.join(output_dir, str(counter) + '.jpeg')
            if not os.path.isfile(im_path):
                img_page = Image(image=img)
                blob = img_page.make_blob('jpeg')

                f = open(im_path, 'w')
                f.write(blob)
                f.close()

                im_paths.append(im_path)
            counter += 1

    # for im_path in im_paths:
    #     output_path = im_path[:-5]
	#
    #     subprocess.Popen(['tesseract', im_path, output_path, 'hocr'])

    return True

def doc_accuracy(parent_dir):
    "Given a directory containing the image files for the pages of a document will return a list of the classifier confidence per page"
    agg_acc, agg_conf, agg_std = (0, 0, 0)
    text = ""
    counter = 0
    pages_text=[]
    num_jpeg = sum(1 for element in os.listdir(parent_dir) if ".jpeg" in element)
    # for element in os.listdir(parent_dir):
    for i in range(num_jpeg):
        element = str(i) + ".jpeg"
        # if element[-5:] == ".jpeg":
        accuracy_metric, average_conf_metric, std_metric, text = accuracy(os.path.join(parent_dir, element))
        pages_text.append(text.encode('utf-8'))
        agg_acc += accuracy_metric
        agg_conf += average_conf_metric
        agg_std +=std_metric
        counter += 1

    open(parent_dir+'.txt', 'w').write("\n".join(pages_text))

    if counter == 0:
        return 0, 0, 0

    return [x/float(counter) for x in [agg_acc, agg_conf, agg_std]]

def doc_db_accuracy(master_dir):
    """calculates accuracy metrics across a number of document folders - each folder corresponds to a document and
    should contain 0.jpeg, 1.jpeg etc"""

    output_dict_list = []
    num_files_complete = 0
    for element in os.listdir(master_dir):
        if os.path.isdir(os.path.join(master_dir, element)):
            document_dir = os.path.join(master_dir, element)
            if any(['.jpeg' in x for x in os.listdir(document_dir)]):
                doc_metrics = doc_accuracy(document_dir)
                if sum(doc_metrics) == 0:
                    continue
                doc_dict = {
                    'name': element,
                    'avg_accuracy': doc_metrics[0],
                    'avg_confidence': doc_metrics[1],
                    'avg_std': doc_metrics[2]
                }
                output_dict_list.append(doc_dict)
                num_files_complete +=1
                f = open('doc_dict.txt', 'w')
                f.write(json.dumps(output_dict_list))
                f.close()
                print('Num complete docs ', num_files_complete)

    sorted_list = sorted(output_dict_list, key=lambda k: k['name'])
    return output_dict_list

def write_to_file(metrics_dict_list, filename = 'output.csv'):
    keys = metrics_dict_list[0].keys()
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(metrics_dict_list)

    return True

if __name__ == "__main__":
    input_dir = sys.argv[1]
    metrics_dict_list = doc_db_accuracy(input_dir)
    print(metrics_dict_list)
    write_to_file(metrics_dict_list)
    print('done writing to file')

