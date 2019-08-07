import cv2
import numpy as np
# from matplotlib import pyplot as plt

img = cv2.imread('0.jpeg')



def compute_skew(image):
    # image = cv2.bitwise_not(image)
  
    shape = np.shape(image)
    height, width = shape[0], shape[1]

    edges = cv2.Canny(image, 150, 200, 3, 5)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=width / 2.0, maxLineGap=20)
    angle = 0.0
    number_of_line = lines.size
    for x1, y1, x2, y2 in lines[0]:
        if x1 != x2:
            angle += np.arctan(y2 - y1 / x2 - x1)

    print ("angle returned here :",  angle)
    return angle / number_of_line



def deskew(image, angle):
    angle = np.math.degrees(angle)
    # image = cv2.bitwise_not(image)
    non_zero_pixels = cv2.findNonZero(image)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)

    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    rows, cols = image.shape
    rotated = cv2.warpAffine(image, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)

    return cv2.getRectSubPix(rotated, (cols, rows), center)





deskewed_image = deskew(img, compute_skew(img))
cv2.imwrite("deskewed.jpg", deskewed_image)

print ("DONE")





#  ------------------------------------------------------------------------


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
 
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# cv2.imwrite("test.jpg", thresh)
# print ("writing test file")


# grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]

print ("angle here : ",  angle)
 
# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
if angle < -45:
	angle = -(90 + angle)
 
# otherwise, just take the inverse of the angle to make
# it positive
else:
	angle = -angle




# # rotate the image to deskew it
# (h, w) = img.shape[:2]
# center = (w // 2, h // 2)
# M = cv2.getRotationMatrix2D(center, angle, 1.0)
# rotated = cv2.warpAffine(img, M, (w, h),
# 	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


# # draw the correction angle on the image so we can validate it
# cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
# 	(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
# # show the output image
# cv2.imwrite("out.jpg", rotated)