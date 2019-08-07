# -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
from tesserocr import PyTessBaseAPI
import numpy as np
import distance




# def compile_words(hocr_file): 

#     f = open(hocr_file, 'r')

#     soup = BeautifulSoup(f, 'html.parser')
#     text = soup.get_text().replace('\n', " ")

#     words = [word.encode('utf-8') for word in text.split()]
#     return words




# def accuracy(hocr_actual, hocr_output): 
#     words_actual = compile_words(hocr_actual)
#     words_output = compile_words(hocr_output)

#     errors = 0

#     for i in range(len(words_output)):
#         correct = words_actual[i]
#         word = words_output[i]

#         if word!= correct:
#             print (word, correct)
#             errors+=1 

#     return 100 - (errors/float(len(words_output)))*100.0


# # print compile_words("/Users/ayushs/Desktop/projects/ocrProject/ocrnet/SampleEmploymentContract/0.hocr")


# f1 = "/Users/ayushs/Desktop/projects/ocrProject/ocrnet/SampleEmploymentContract/0.hocr"
# f2 = "/Users/ayushs/Desktop/projects/ocrProject/ocrnet/SampleEmploymentContract/1.hocr"


# print accuracy(f1,f2) 


def accuracy_levenshtein(text_1, text_2):
    t_1_words = text_1.replace('\n', '').split(' ')
    t_2_words = text_2.replace('\n', '').split(' ')
    return distance.levenshtein(t_1_words, t_2_words)

def accuracy_confidence(image_file, threshold = 85):
    print('running ocr')
    with PyTessBaseAPI(lang='eng') as api:
        api.SetImageFile(image_file)
        conf = api.AllWordConfidences()
        text = api.GetUTF8Text()

    conf_np = np.array(conf)
    error = 0 

    print('aggregating error')
    for word_accuracy in conf: 
        if word_accuracy < threshold:
            error +=1 

    if len(conf) == 0:
        return 0, 0, 0, text
    accuracy_metric = 100 - error/float(len(conf))*100

    average_conf_metric = np.mean(conf_np)
    std_metric = np.std(conf_np)

    return accuracy_metric, average_conf_metric, std_metric, text


if __name__ == "__main__":

    test = "/Users/nischalnadhamuni/Documents/Classes-Fall-2017/6.819/ocrnet/test_docs_jpg/0/0.jpeg"
    print accuracy(test)






