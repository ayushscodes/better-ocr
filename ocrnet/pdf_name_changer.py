import os
import subprocess
import sys
from run import pdf_2_jpeg

parent_directory = sys.argv[1]

counter = 0
for i in range(len(os.listdir(parent_directory))):
	element = os.listdir(parent_directory)[i]
	# doc_metrics = {'filename': element}
	# metrics_list.append(doc_metrics)

	# if ".pdf" in element:
	# 	command = " ".join(['mv', '\"'+parent_directory+element+'\"', parent_directory + str(counter)+'.pdf'])
	# 	print(command)
	# 	subprocess.Popen(command, shell=True)
	# 	counter += 1

	if ".pdf" in element:
		pdf_2_jpeg(os.path.join(parent_directory, element))
		counter+=1
