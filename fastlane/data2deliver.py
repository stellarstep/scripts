#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml, os, codecs, argparse
import re, mdpatterns
from os.path import expanduser
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

parser = argparse.ArgumentParser(description='Write deliver resouce files from metadata.yml')
parser.add_argument('bundle', help='Target fastlane path')
parser.add_argument('fastlane', help='fastlane path')
args = parser.parse_args()

#names
__project__ = os.getcwd()
__dirpath__ = os.path.join(__project__, expanduser(args.fastlane))
__ignore_keys__ = ["notices"]
__deliver_file__ = os.path.join(__dirpath__,'Deliverfile')
__data__ = yaml.safe_load(open(os.path.join(__dirpath__,'metadata.yml')))

datas = __data__[args.bundle]
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
		for key, value in [(d, data_lang[d]) for d in data_lang]:
			#pass if key contains by ignore keys
			if key in __ignore_keys__:
				continue
			#remove markdown link tags
			for m in re.finditer(mdpatterns.LINK_RE, value, re.S):
				value = value.replace(m.group(0), m.group(1))
			#remove html tags blocks
			value = re.sub('<[^<]+?>', '', value)
			#base
			p = os.path.join(__dirpath__, args.bundle, l, key+'.txt')
			f = codecs.open(p, 'w', 'utf-8')
			f.write(value)
			f.close()
			print p,'<-',value

#write deliver file
deliver_file_lines = ''
taphead = None
current_lines_app_target_id = None
for line in codecs.open(__deliver_file__,'r','utf-8').readlines():
	if 'app_identifier' in line:
		taphead = line.split('app_identifier')[0]
		current_lines_app_target_id = line.split('app_identifier')[1].strip().replace('"','')
		assert current_lines_app_target_id is not None, 'app_identifier not found. "app_identifier" must be available at first line of each bundle ids'
		deliver_file_lines += line
		# if current_lines_app_target_id == args.bundle:
		# 	deliver_file_lines += ''.join([taphead, 'app_version', ' ','"', __data__[current_lines_app_target_id]['version'],'"','\n'])
		continue

	if current_lines_app_target_id == args.bundle:
		if not 'app_version' in line:
			deliver_file_lines += line
	else:
		deliver_file_lines += line

wf = codecs.open(__deliver_file__, 'w','utf-8')
wf.writelines(deliver_file_lines)
wf.close()
print deliver_file_lines
