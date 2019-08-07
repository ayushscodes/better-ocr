import subprocess
import os
from wand.image import Image
from PIL import Image as PI
import sys
import pyPdf
from fade_text.fade import apply_fade


#citation https://groups.google.com/forum/#!topic/tesseract-ocr/mDMXBmpay9E

def pdf_2_tif(input_pdf):
	combined_tiff = input_pdf[:-3]+'tif'

	if os.path.isfile(combined_tiff):
		return combined_tiff

	# image_pdf = Image(filename=input_pdf, resolution=300)
	reader = pyPdf.PdfFileReader(open(input_pdf))
	num_pages =  reader.getNumPages()
	tifs = []
	for i in range(num_pages):
		output_tif = input_pdf[:-4] + '_{}.tif'.format(str(i))
		tifs.append(output_tif)
		command = " ".join(['convert',
						  '-depth','4',
						  '-density', '300',
						  '-flatten',
						  '+matte',
						  input_pdf + '[{}]'.format(str(i)),
						  output_tif
						  ])
		subprocess.Popen(command, shell=True).wait()

	concat_command = 'convert ' + " ".join(tifs) + " " + combined_tiff
	subprocess.Popen(concat_command, shell=True).wait()

	for file in tifs:
		subprocess.Popen('rm -rf '+ file, shell=True)

	# output_tif = input_pdf.replace('.pdf', '.tif')
	# image_pdf.save(filename=output_tif)
	return combined_tiff


def create_font_properties(lang_name, italic=False, bold=True, fixed=False, serif=True, fraktur=False):
	string = " ".join([lang_name, str(int(italic)), str(int(bold)), str(int(fixed)), str(int(serif)), str(int(fraktur))])
	subprocess.Popen('echo \"' + string + '\" >> font_properties', shell=True).wait()
	return True

def create_box_file(tif_file):
	"returns the name of the new box file"
	box_file = tif_file[:-3]+'box'
	if os.path.isfile(box_file):
		return box_file

	if tif_file[-3:] != 'tif':
		raise ValueError("A tif file must be passed as a parameter")
	subprocess.Popen(['tesseract', tif_file, tif_file[:-4], 'batch.nochop', 'makebox']).wait()
	subprocess.Popen(['mv', tif_file[:-3]+'txt', tif_file[:-3]+'box']).wait()
	return tif_file[:-3]+'box'

def create_train_file(tif_file):
	"returns the name of the training file"
	subprocess.Popen(['tesseract', tif_file, tif_file[:-4], 'nobatch', 'box.train']).wait()
	return tif_file[:-3] + "tr"

def cluster(train_file):
	'the below two calls will produce "inttemp", "pffmtable", "Microfeat" (not used) and normproto '
	subprocess.Popen(['mftraining', train_file]).wait()
	subprocess.Popen(['cntraining', train_file]).wait()

def compute_char_set(box_file):
	"this wil generate a unicharset file"
	subprocess.Popen(['unicharset_extractor', box_file]).wait()
	return "unicharset"

def create_dict_data():
	subprocess.Popen(['touch', 'frequent_words_list']).wait()
	subprocess.Popen(['touch', 'words_list']).wait()
	subprocess.Popen(['wordlist2dawg', 'frequent_words_list', 'freq-dawg']).wait()
	subprocess.Popen(['wordlist2dawg', 'words_list', 'word-dawg']).wait()
	return True

def rename_files(lang_name):
	subprocess.Popen('mv normproto ' + lang_name + '.normproto', shell=True).wait()
	subprocess.Popen('mv pffmtable ' + lang_name + '.pffmtable', shell=True).wait()
	subprocess.Popen('mv inttemp ' + lang_name + '.inttemp', shell=True).wait()
	subprocess.Popen('mv unicharset ' + lang_name + '.unicharset', shell=True).wait()
	subprocess.Popen('mv shapetable ' + lang_name + '.shapetable', shell=True).wait()
	return True

def combine_file(lang_name):
	subprocess.Popen('combine_tessdata ' + lang_name + '.', shell=True).wait()
	return lang_name+'.traineddata'

def move_traineddata(traineddata_file, tessdata_dir='/usr/share/tesseract-ocr/tessdata/'):
	command = ' '.join(['cp', traineddata_file, tessdata_dir])
	subprocess.Popen(command, shell=True).wait()
	return True

def augment_doc(input_tif):
	if input_tif[-3:] != 'tif':
		raise ValueError ('a tif file must be fed as input to the augment doc function')

	command = 'convert ' + input_tif + ' ' + input_tif[:-4] + '-%d.tif'
	print(command)
	subprocess.Popen('convert ' + input_tif + ' ' + input_tif[:-4] + '-%d.tif', shell=True).wait()
	num_pages = get_num_pages(input_tif)

	page_tifs = []
	for i in xrange(num_pages):
		page_tif = input_tif[:-4] + '-{}.tif'.format(i)
		print(page_tif)
		apply_fade(page_tif, page_tif)
		page_tifs.append(page_tif)

	page_tifs = ' '.join(page_tifs)
	subprocess.Popen('convert ' + page_tifs + ' ' + input_tif, shell=True).wait()
	return input_tif

def get_num_pages(input_tif):
	'returns the number of pages in a tif file'
	temp_file = 'temp_file.txt'
	subprocess.Popen('identify -format "%p" ' + input_tif + ' > ' + temp_file, shell=True).wait()
	return len(open(temp_file, 'r').read())

def train_model(input_pdf, augment_image=False):
	lang_name = "fade"
	tessdata_dir = '/usr/share/tesseract-ocr/tessdata/'

	print('create font properties')
	create_font_properties(lang_name)

	print('pdf_2_tif')
	tif = pdf_2_tif(input_pdf)
	print('tif file is ', tif)

	print('create_box_file')
	box = create_box_file(tif)
	print('box file is ', box)

	if augment_image:
		modified_tif = augment_doc(tif)
		print('create_train_file')
		tr = create_train_file(modified_tif)
		print("train file is ", tr)
	else:
		tr = create_train_file(tif)

	print('compute_char_set')
	compute_char_set(box)

	print('cluster')
	cluster(tr)

	# print('create_dict_data')
	# create_dict_data()

	print('renaming files with lang name prefix')
	rename_files(lang_name)

	print('combine to create traineddata file')
	traineddata_file = combine_file(lang_name)

	print('move traineddata file to tessdata dir')
	move_traineddata(traineddata_file, tessdata_dir)

	print('Done')
	return True

if __name__ == "__main__":
	#input_tif = sys.argv[1]
	#print(augment_doc(input_tif))
	input_pdf = sys.argv[1]
	train_model(input_pdf)