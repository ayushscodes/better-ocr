import numpy as np 
import cv2
import os


np.set_printoptions(threshold=np.nan)



def detect_whitespace(column, threshold = 0.90):
	shape = np.shape(column)
	height = shape[0]	
	count_whites = 0

	for elt in column:
		if elt == 255:
			count_whites+=1

	if count_whites/float(height) > threshold:

		return True

	return False



def whitespace_column(column_size, width = 6):


	array = [255 for i in range(column_size)]
	np_array = np.array(array)
	np_concat = np.array(array).reshape([column_size, 1])
	np_array = np.reshape(array, [column_size,1])


	for i in range(width-1):
		np_array = np.concatenate((np_array, np_concat),axis = 1)

	# print ("here ---afaf-", np.shape(np_array))
	return np_array 




def binarise(image): 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(image, 0,255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	return thresh



def seperate_words(image, threshold, whitespace_width): 
	shape = np.shape(image)
	height, width = shape[0], shape[1]
	# print (height, width)

	out_image = np.array([255 for i in range(height)]).reshape([height, 1])

	# print ("shape out image ", np.shape(out_image))


	for i in range(width -1) :
		current_column = image[:,i].reshape([height,1])
		current_whitespace = detect_whitespace(current_column, threshold = threshold)

		if current_whitespace:
			# print ("here--------")
			# print ("current_column whitespace ", current_column)
			next_column = image[:,i+1]
			next_whitespace = detect_whitespace(next_column)

			if next_whitespace:
				whitespace = whitespace_column(height, width = whitespace_width)
				# print (whitespace)
				out_image = np.concatenate((out_image,whitespace), axis = 1)

		else:
			# print ("here")
			# print (np.shape(out_image), np.shape(current_column))
			out_image = np.concatenate((out_image, current_column), axis = 1)
			# print (current_column)
			# print ("come here 1")

	return out_image

		





def run_segment_words(image_file, threshold, whitespace_width):
	print('image file is ', image_file)

	image = cv2.imread(image_file)


	# print ("input image", image)
	image = binarise(image)
	# print ("size binarised", np.shape(image))
	# print ("binarised --- ", image)

	out_image = (seperate_words(image, threshold, whitespace_width))
	out_file, extension = os.path.splitext(image_file)
	#str(filter(str.isdigit, image_file))
	out_file = out_file + "_seperated" + extension
	cv2.imwrite(out_file, out_image)

	return out_file





