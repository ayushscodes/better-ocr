# -*- coding: utf-8 -*-
import subprocess
import os
from sets import Set
from segment_words import run_segment_words
import sys
import editdistance 


threshold = 0.9
whitespace_width = 5

def classify(labeled_file, im_parent_dir, seperate_char=True, output_log='char_split_acc.txt'):
	"""labeled file - the file linking image file names to the words they contain
	im_parent_dir = the parent directory holding the directories with the images
	"""



	f = open(output_log, 'w')
	pages_set_list = []
	pages_dir_names =[]
	for element in sorted(os.listdir(im_parent_dir)):
		page_dir = os.path.join(im_parent_dir, element)
		if os.path.isdir(page_dir):
			files = os.listdir(page_dir)
			if any(['.PNG' in x for x in files]):
				pages_set_list.append(Set(files))
				pages_dir_names.append(page_dir)
	annotations = open(labeled_file, 'r').read().strip().splitlines()
	print(annotations)
	print('page dir names ', pages_dir_names)
	pages_dir_names = sorted(pages_dir_names)
	print('sorted array is ', pages_dir_names)
	page_index = 0
	temp_file = 'single_word_buffer.txt'
	f.write('\t'.join(['file_name', 'actual_word', 'tes_normal', 'tes_char_segmentation', '\n']))
	for annotation in annotations:
		file_name, label = annotation.split(' ')
		print('file name is ', file_name)
		im_page_dir = pages_dir_names[page_index]
		page_set = pages_set_list[page_index]
		print('first page dir is ', im_page_dir)
		if file_name not in page_set:
			page_index+=1
			im_page_dir = pages_dir_names[page_index]
			page_set = pages_set_list[page_index]
			print('second page dir is ', im_page_dir)
			if file_name not in page_set:
				raise RuntimeError('seems to be a page jump')


		im_file_path = os.path.join(im_page_dir, file_name)
		augmented_image = run_segment_words(im_file_path, threshold, whitespace_width)
		ayush_word = tes_single_word(augmented_image, temp_file)
		if ayush_word.strip() == '':
			ayush_word = 'NONE'

		tes_word = tes_single_word(im_file_path, temp_file)
		if tes_word.strip() == '':
			tes_word = 'NONE'

		actual_word = label
		f.write('\t'.join([file_name, actual_word, tes_word, ayush_word, '\n']))

	f.close()

	return


def tes_single_word(im_file, temp_file):
	subprocess.Popen('rm -f ' + temp_file, shell=True).wait()
	command = ' '.join(['tesseract', im_file, temp_file.split('.')[0], '-l eng --psm 8'])
	subprocess.Popen(command, shell=True).wait()
	f = open(temp_file, 'r')
	word = f.read().strip()
	f.close()

	return word




def accuracy_runner(acc_file):
	content = []

	accuracy_runner_output = "accuracy_runner_output.txt"	

	with open(acc_file) as f:
		content = f.read().strip().splitlines()
		content = [x.strip("\n") for x in content]
		content = [x.strip("\t") for x in content]
		content = [x.split() for x in content]




	tes_word_dist_vector = []
	tes_char_segword_dist_vector = []
	bad_tes_word_vector = [] 
	bad_char_segword_vector = []


	for i in range(1, len(content)-1):
		print('content[i] is ', content[i])
		file_name =  unicode(content[i][0], 'utf-8')
		actual_word = unicode(content[i][1], 'utf-8')
		tes_word = unicode(content[i][2], 'utf-8')
		print ("tes word ", tes_word)
		tes_char_segword = unicode(content[i][3], 'utf-8')

		tes_word_dist, tes_char_segword_dist = accuracy_metric(actual_word, tes_word, tes_char_segword)

		tes_word_dist_vector.append(tes_word_dist)
		tes_char_segword_dist_vector.append(tes_char_segword_dist)

		if tes_word_dist > len(actual_word)/2:
			bad_tes_word_vector.append([file_name, tes_word, tes_char_segword])
			print ("word here -- ", tes_word)
		if tes_char_segword_dist > len(actual_word)/2:
			bad_char_segword_vector.append([file_name, tes_word, tes_char_segword])

	f = open(accuracy_runner_output, 'w')
	f.write('\n'.join([str(tes_word_dist_vector), str(tes_char_segword_dist_vector), str(bad_tes_word_vector), str(bad_char_segword_vector)]))

	return (sum(tes_word_dist_vector)/float(len(tes_word_dist_vector))), (sum(tes_char_segword_dist_vector)/float(len(tes_char_segword_dist_vector)))


	


def accuracy_metric(actual_word, tes_word, tes_char_segword): 

	if tes_word == "NONE":
		tes_word = ""
	if tes_char_segword == "NONE":
		tes_char_segword = ""
		

	tes_word_dist = int(editdistance.eval(tes_word, actual_word))
	tes_char_segword_dist = int(editdistance.eval(tes_char_segword, actual_word))
	return tes_word_dist, tes_char_segword_dist






if __name__ == "__main__":
	# python char_split_accuracy.py ../allWork/labeled_words_mini.txt ../words_data/
	labeled_file = sys.argv[1]
	im_parent_dir = sys.argv[2]
	classify(labeled_file, im_parent_dir, seperate_char=True)

	testFile = 'char_split_acc.txt'
	print (accuracy_runner(testFile))







