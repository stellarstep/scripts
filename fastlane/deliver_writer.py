#!/usr/bin/python
'''
[example : metadata.yml]
en-US:
	metadata_dir_app1:
			name: App Name
   marketing_url: http://url.com
ja:
	metadata_dir_app1:
			name: Japanese App Name
   marketing_url: http://url.com

[result]
fastlane/metadata_dir_app1/name.txt <- 'App Name'
fastlane/metadata_dir_app1/marketing_url.txt <- 'http://url.com'
'''

import yaml, os, codecs

#names
__dirpath__=os.path.dirname(os.path.realpath(__file__))
datas = yaml.safe_load(open(os.path.join(__dirpath__,'metadata.yml')))
datas_base = datas['Base'] if 'Base' in datas else None

def dict_merge(dct, merge_dct):
	for k, v in merge_dct.iteritems():
		if (k in dct and isinstance(dct[k], dict)
				and isinstance(merge_dct[k], dict)):
			dict_merge(dct[k], merge_dct[k])
		else:
			dct[k] = merge_dct[k]

for dir, a, files in os.walk(__dirpath__):
	l = os.path.basename(dir)
	if l in datas:
		data_lang = datas[l]
		dict_merge(data_lang, datas_base)
		for app, meta in [(k, data_lang[k]) for k in data_lang]:
			for mfile in meta:
				#base
				p = os.path.join(__dirpath__, app, l, mfile+'.txt')
				f = codecs.open(p, 'w', 'utf-8')
				f.write(meta[mfile])
				f.close()
				print p,'\n',meta[mfile],'\n'
