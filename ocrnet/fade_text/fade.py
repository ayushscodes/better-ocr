import numpy as np 
import cv2

def apply_fade(image_file, output_name, fade_level = 25):

	image = cv2.imread(image_file, 0)

	shape = np.shape(image)
	rows, cols = shape[0], shape[1]

	for i in range(rows): 
		for j in range(cols):
			randomInt = np.random.randint(0,100)
			if randomInt < fade_level:
				image[i][j] = 255

	cv2.imwrite(output_name, image)
	return output_name



# fade_level = 60

# test = "testTiff.tiff"
# faded_image = apply_fade(test, fade_level = fade_level)

# file_name = ("faded_image" + str(fade_level) + ".tiff")

# cv2.imwrite(file_name, faded_image)



