import subprocess

lang_name = 'fade'
input_file = 'SampleEmploymentContract.pdf'
base_name = input_file[:-4]
files_to_delete = ' '.join([base_name+'.tif', base_name+'.tr', base_name+'.box', base_name + "_aug.*", base_name + "-*",
					'inttemp', 'shapetable', 'font_properties', 'pffmtable', 'unicharset', 'frequent_words_list', 'words_list', 'normproto',
				   lang_name+'.inttemp', lang_name+'.shapetable', lang_name+'.font_properties', lang_name+'.pffmtable', lang_name+'.normproto',
				  lang_name + '.unicharset', lang_name+'.frequent_words_list', lang_name+'.words_list', lang_name+'.traineddata'])

command = subprocess.Popen('rm -f ' + files_to_delete, shell=True)