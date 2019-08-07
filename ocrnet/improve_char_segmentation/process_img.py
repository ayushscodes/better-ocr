import numpy as np
import os
import scipy.misc
from scipy import ndimage
import scipy.ndimage
from random import choice, randint
from scipy.ndimage.interpolation import zoom
import PIL 



#update as we add transforms
transform_list = ["deskew", "border", "noise_removal"]




def noise_image(image):
	out_image = image 
	# change code to apply transformation 

	return out_image




def deskew_image(image):
	out_image = image 
	# change code to apply transformation 

	return out_image



def border_image(image):
	leftX
	out_image = image 
	# change code to apply transformation 

	return out_image




def process_image(image, transform = []):
	'''
	compose transforms provided in transform and output image
	'''
	out_image = image

	if "noise_removal" in transform:
		out_image = noise_image(image)
	#scipy.misc.imsave(os.path.join('./', 'image_trans/blurred.jpg'), blurred_image)
	if "border" in transform:
		out_image = border_image(out_image)
	#scipy.misc.imsave(os.path.join('./', 'image_trans/zoomed.jpg'), zoomed_image)
	
	if "deskew" in transform:
		out_image = deskew_image(out_image)
		#scipy.misc.imsave(os.path.join('./', 'image_trans/flipped.jpg'), flipped_image)
	

	# add more blocks for further transformations

	return out_image




'''
Testing ------------------------------------------------
''' 














