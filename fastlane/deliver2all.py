#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
python deliver_rnote.py com.stells.*
'''

import yaml, os, codecs, time, datetime,re,argparse,textwrap, subprocess
from datetime import date, timedelta
from time import mktime
from os.path import expanduser
from shutil import copyfile

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

parser = argparse.ArgumentParser(description='Deploy information to release Jekyll.')
parser.add_argument('bundle', help='Bundle id for targeted app')
parser.add_argument('fastlane', help='Target fastlane path')
parser.add_argument('jekyll', help='Target jekyll path')
parser.add_argument('-f','--force', type=bool, help='Something forceful.', default=None, required=False, nargs='*')
parser.add_argument('-s','--screenshots', type=str, help='screenshots path.', default=None, required=False, nargs='*')
parser.add_argument('-ps','--presskitscreenshots', type=str, help='press kit screenshots path.', default=None, required=False, nargs='*')
parser.add_argument('-l','--l10n', type=str, help='l10n resource path.', default=None, required=False, nargs='*')
args = parser.parse_args()

__force__= args.force is not None
__project__ = os.getcwd()
__dirpath__ = os.path.join(__project__, expanduser(args.fastlane))
__target_bundle__=args.bundle
# python ~/Documents/scripts/fastlane/deliver2all.py com.stells.giff fastlane '~/Documents/giffwww'  -s '~/Documents/giff-resources/appstore/screenshots/giff' -ps '~/Documents/aniart-presskit/screenshots' -l 'giff/res/l10n'
__www__=expanduser(args.jekyll)
__screenshots__=expanduser(args.screenshots[0]) if args.screenshots is not None else None
__presskit_screenshots__=expanduser(args.presskitscreenshots[0]) if args.presskitscreenshots is not None else None
__l10n__=os.path.join(__project__, expanduser(args.l10n[0])) if args.l10n is not None else None

#www
__www_config__ = yaml.safe_load(open(os.path.join(__www__,'_config.yml')))
__note_file__='release_notes.txt'
__notice_src_file__='notices.txt'
__replace_targets__=[(u'\u2022', '-'),('+', '-')]

#data
__data_file__=os.path.join(__project__,args.fastlane,'metadata.yml')
__data__=yaml.safe_load(open(__data_file__))
__default_target_key__='default_target'
__default_target_bundle___=__data__[__default_target_key__]
__global_notices_key__='global_notices'
__local_notices_key__="notices"
__prefix_ignore_after_lines__='Highlights of the previous update'

__targetdata__ = __data__[__target_bundle__]
__targetdata_base__ = __targetdata__['Base'] if 'Base' in __targetdata__ else None
__version__=__targetdata__['version']

def get_target_data(bundle_id):
	return __data__[bundle_id]

def get_www_lang(lang):
	el_langs=__www_config__['langs']
	for el, elpath in [(k, el_langs[k]['path']) for k in el_langs]:
		if el in lang: return (el, elpath)
	return None

def file_dir(file_path):
	_dir = os.path.dirname(file_path)
	if not os.path.exists(_dir):
		os.mkdir(_dir)
	return file_path

def open_file(file_path):
	return codecs.open(file_dir(file_path), 'w', 'utf-8')

def copy_file(src_file, dest_file):
	return copyfile(src_file, file_dir(dest_file))

'''
	Web - common
'''
#common
def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def get_mdate_from_file(file_path):
	mtime = os.path.getmtime(file_path)
	#-timedelta(days=1)
	return (datetime.datetime.utcfromtimestamp(mtime)).strftime("%Y-%m-%d")

def get_current_date_stamp():
	return datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

def get_content_for_markdown(content_str):
	if not is_ascii(content_str):
		content_str = content_str.encode('utf8')

	content_str = content_str.decode('utf8')

	#replace chars
	for s, r in __replace_targets__:
		content_str= content_str.replace(s,r).strip()

	#filtering lines
	content_str_by_line = ''
	for line in content_str.splitlines(True):
		#stop if matched lines
		if line.strip().startswith(__prefix_ignore_after_lines__):
			if len(content_str_by_line.splitlines(True)):
				content_str = content_str_by_line
			break
		content_str_by_line += line

	return content_str

def get_content_for_markdown_of_file(file):
	if not file:
		return None
	f = os.path.join(dir,file)
	o_content = get_content_for_markdown(open(os.path.join(dir,file)).read())
	return (o_content, get_mdate_from_file(f)) if o_content else None

def get_value_from_target_data(lang, key):
	return __targetdata__[lang][key] if lang in __targetdata__ and key in __targetdata__[lang] else None

#posts
def get_post_file(entities):
	return '-'.join(entities)+'.md'

def get_post_file_abs_path(filename):
	return os.path.join(__www__, '_posts', filename)

def find_post_file(containing_filename):
	return find_post_file_by_target(None, containing_filename)

def find_post_file_by_target(target, containing_filename):
	for d,a,f in os.walk(get_post_file_abs_path(target if target else '')):
		for _f in f:
			if containing_filename in _f:
				return os.path.join(d, _f)
	return None

#notice
def get_global_notice_data():
	return __data__[__global_notices_key__] if __global_notices_key__ in __data__ else None

#site data
def deploy_to_www_site_data(bundle):
	datas_default = get_target_data(bundle)
	data_file_path = os.path.join(__www__,'_data')
	for www_data_file in [f for d, a, f in os.walk(data_file_path)][0]:
		if www_data_file.startswith('.') or not os.path.isfile(os.path.join(data_file_path, www_data_file)):
			continue

		data_file_lang = os.path.splitext(www_data_file)[0]
	 	data_of_file_lang = (filter(lambda lang: data_file_lang in lang, datas_default) or ['Base'])[0]
		data_titie = 'Untitled'
		if 'name' in datas_default[data_of_file_lang]:
			data_titie = datas_default[data_of_file_lang]['name']
		elif 'name' in datas_default['Base']:
			data_titie = datas_default['Base']['name']
		data_lines=[]
		#read
		rf = codecs.open(os.path.join(data_file_path, www_data_file), 'r','utf-8')
		for line in rf.readlines():
			if 'page_title:' in line:
				new_title = 'page_title: "'+data_titie+'"'
				data_lines.append(new_title+'\n')
				print rf.name, '<', new_title
			else:
				data_lines.append(line)
		rf.close()
		#write
		wf = codecs.open(os.path.join(data_file_path, www_data_file), 'w','utf-8')
		wf.writelines(data_lines)
		wf.close()

'''
	Site data
'''
# site data -> _data/{lang}.yml
print '[Site Data]', __default_target_bundle___, __target_bundle__
if __default_target_bundle___ == __target_bundle__:
	deploy_to_www_site_data(__target_bundle__)



'''
	Release notess
'''
# post -> _post/{target}/{lang}.md
print '[Release notes]'
for dir, a, files in os.walk(__dirpath__):
	target = os.path.basename(os.path.dirname(dir))
	data_lang=os.path.basename(dir)
	langs = get_www_lang(data_lang)
	#find from deliver file
	lang, lang_p=None,None
	if langs: lang, lang_p = langs
	if not (lang and lang_p):
		continue

	#release note
	def __deploy_release_notes():
		existed_file = find_post_file_by_target(target, get_post_file(['Release', __version__, lang]))
		#skip if same note of same version
		if not __force__ and existed_file:
			return
		#content from overriden metadata
		content, mdate = get_content_for_markdown(get_value_from_target_data(data_lang, 'release_notes')), get_mdate_from_file(os.path.join(dir, __note_file__))
		#content from original deliver metadata
		if not content:
			content, mdate = get_content_for_markdown_of_file(__note_file__)
		#skip if content is empty
		if not content or not mdate:
			return

		#clean exist
		if existed_file:
			os.remove(existed_file)
		#post
		of = open_file(os.path.join(__www__, '_posts', target, get_post_file([mdate, 'Release', __version__, lang])))
		of.write(content.strip())
		of.close()

		#html
		hf = open_file(os.path.join(__www__, 'notes', target, lang_p[1:]+'.html'))
		hf.write(textwrap.dedent(
		"""\
		---
		layout: note
		lang: {0}
		version: {1}
		modified: {2}
		---
		""".format(lang, __version__, get_current_date_stamp())))
		hf.close()
		print of.name
		print hf.name

	#notice
	global_notice_data = get_global_notice_data()
	has_global_notice = global_notice_data is not None and data_lang in global_notice_data
	def __deploy_notices(notice_src_file_exists):
		local_notice_file = find_post_file_by_target(target, get_post_file(['Notice', lang]))

		def __get_notice_filepath(_mdate):
			return os.path.join(__www__, '_posts', target, get_post_file([_mdate, 'Notice', lang]))

		#skip if same note of same version
		if not local_notice_file and not has_global_notice:
			return

		content, mdate = None, None

		# primary : content from overriden metadata
		content, mdate = get_value_from_target_data(data_lang, __local_notices_key__), get_mdate_from_file(__data_file__)

		# fallback : content from global notice data if exist
		if not content and has_global_notice:
			content, mdate = global_notice_data[data_lang], get_mdate_from_file(__data_file__)

		# fallback : content from original deliver metadata if not exist in metadata.yml.
#		if not content and notice_src_file_exists:
#			content, mdate = get_content_for_markdown_of_file(__notice_src_file__)

		#else, stop.
		if not content:
			if local_notice_file:
				os.remove(local_notice_file)
			return

		#post
#		if local_notice_file:
#			#remove exist notice if added a force option
#			os.remove(local_notice_file)

		of = open_file(__get_notice_filepath(mdate))
		of.write(content.strip())
		of.close()

		#html
		hf = open_file(os.path.join(__www__, 'notes', target, lang_p[1:]+'.html'))
		hf.write(textwrap.dedent(
		"""\
		---
		layout: note
		lang: {0}
		version: {1}
		modified: {2}
		---
		""".format(lang, __version__, get_current_date_stamp())))
		hf.close()

		print of.name

	if target == __target_bundle__:
		# release note
		if __note_file__ in files:
			__deploy_release_notes()

		# notices
		__deploy_notices(__notice_src_file__ in files)

'''
	Global Notices
'''
print '[Global Notices]'

global_notice_data = get_global_notice_data()
if global_notice_data:
	for lang in global_notice_data:

		c = global_notice_data[lang]
		l,lp = get_www_lang(lang)
		nf = get_post_file([get_mdate_from_file(__data_file__), 'Notice', l])
		f = find_post_file(nf)
		needs_new = not f and c

		#clean previous if setted force
		existed_file = find_post_file_by_target(None, get_post_file(['Notice', l]))
#		if c and existed_file:
#			os.remove(existed_file)

		#start wirte
		ff = open_file(get_post_file_abs_path(nf))
		ff.write(c)
		ff.close()
		print ff.name, ' < ' ,f, c

else:
	basepath = get_post_file_abs_path('')
	for d,r,f in os.walk(basepath):
		for _f in f:
			if not os.path.basename(d).strip() and 'Notice' in _f and '.md'==os.path.splitext(_f)[1]:
				os.remove(os.path.join(d,_f))



'''
	PressKit
'''
# screenshots -> {project}-presskit/screenshots_appstore/*
if __screenshots__ and __target_bundle__ == __default_target_bundle___:
	print '[PressKit]'
	for d, a, f in os.walk(__screenshots__):
		for _f in filter(lambda n: 'Screenshot-750x1334.png' in n, f):
			if __presskit_screenshots__:
				df = os.path.join(__presskit_screenshots__, os.path.basename(d), _f)
				copy_file(os.path.join(d,_f), df)
				print df


'''
	.strings
'''
if __l10n__:
	print '[.strings]',__l10n__
	string_targetdata = get_target_data(__default_target_bundle___)
	__marketing_title_prefix__='"STAppMarketingTitle"'
	for d, a, f in os.walk(__l10n__):
		for _f in filter(lambda n: 'InfoPlist.strings' in n, f):
			langcode = os.path.splitext(os.path.basename(d))[0].replace('_','-')
			lang = langcode.split('-')[0]
			matched_langs = filter(lambda key: key.split('-')[0] == lang, string_targetdata)
			matched_lang = matched_langs[0] if len(matched_langs) else 'Base'

			#zh care
			if lang == 'zh':
				_zh_matched_lang = None
				if langcode in ['zh-CN']:  _zh_matched_lang = 'zh-Hans'
				elif langcode in ['zh-TW','zh-HK']:  _zh_matched_lang = 'zh-Hant'
				#if zh familiy contains string_targetdata
				if _zh_matched_lang and _zh_matched_lang in string_targetdata:
					matched_lang = _zh_matched_lang

			#get data
			matched_data = string_targetdata[matched_lang]

			df = os.path.join(__l10n__, os.path.basename(d), _f)
			# default from 'Base'
			new_marketing_title = ('name' in matched_data and matched_data['name']) or ('name' in __targetdata_base__ and __targetdata_base__['name'])

			if new_marketing_title:
				data_lines=[]
				#read
				rf = codecs.open(df, 'r','utf-8')
				for line in rf.readlines():
					if __marketing_title_prefix__ in line:
						new_title = __marketing_title_prefix__+' = "'+new_marketing_title+'";'
						data_lines.append(new_title+'\n')
						print rf.name, ' < ' ,new_title
					else:
						data_lines.append(line)
				rf.close()
				#write
				wf = codecs.open(df, 'w','utf-8')
				wf.writelines(data_lines)
				wf.close()
