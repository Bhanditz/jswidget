#!/usr/bin/python
# This takes template.html and makes a document.write() for it.
# Later, it could take template.html and make DOM objects instead.

import re
from simpletal import simpleTAL, simpleTALES
import cStringIO as StringIO
import os
import BeautifulSoup

LANGUAGE="en_US"

import sys
sys.path.insert(0, './license_xsl/licensexsl_tools')
import translate

def grab_license_ids():
	licenses_xml = BeautifulSoup.BeautifulSoup(open('license_xsl/licenses.xml'))
	juris = []
	for juri in licenses_xml('jurisdiction-info'):
		juris.append(juri['id'])
	juris = [juri for juri in juris if juri != '-']
	return juris

def get_PoFile(language):
	return translate.PoFile("license_xsl/i18n/i18n_po/icommons-%s.po" % language)

def country_id2name(country_id, language):
	# Now gotta look it up with gettext...
	po = get_PoFile(language)
	try:
		return unicode(po['country.%s' % country_id], 'utf-8')
	except KeyError:
		return country_id

def escape_single_quote(s):
	return s.replace("'", "\\'")

def xml_asciify(u):
	out = ''
	for char in u:
		if ord(char) < 128:
			out += char
		else:
			out += '&#%d;' % ord(char)
	return out
	

def extremely_slow_translation_function(s, out_lang):
	# First, look through the en_US po for such a string
	en_po = get_PoFile('en_US')
	found_key = None
	for entry in en_po.strings:
		if en_po.get(entry, -1) == s:
			found_key = entry

	real_po = get_PoFile(out_lang)
	return real_po.get(found_key, s)
	# Return the version in out_lang's PO.

def expand_template_with_jurisdictions(templatefilename, juridict):
	# Create the context that is used by the template
	context = simpleTALES.Context()
	context.addGlobal("jurisdictions", juridict)

	templateFile = open('template.html')
	template = simpleTAL.compileXMLTemplate(templateFile)
	templateFile.close()
	
	output_buffer = StringIO.StringIO()
	template.expand(context, output_buffer, 'utf-8')
	return output_buffer.getvalue()

def translate_spans_with_only_text_children(spans, lang):
	for span in spans:
		if len(span.childNodes) == 1:
			child = span.childNodes[0]
			if child.nodeType == 3: # FIXME: Magic number
						# maybe means Text
						# node?
				child.data = extremely_slow_translation_function(child.data, lang)


def gen_templated_js(language):
	jurisdiction_names = grab_license_ids()
	jurisdictions = [ dict(id=juri, name=country_id2name(juri, language)) for juri in jurisdiction_names]

	from xml.dom.minidom import parse, parseString
	expanded = expand_template_with_jurisdictions('template.html', jurisdictions)
	expanded_dom = parseString(expanded)

	# translate the spans, then pull out the changed text
	translate_spans_with_only_text_children(expanded_dom.getElementsByTagName('span'), language)
	out_tmp = StringIO.StringIO()
	translated_expanded = expanded_dom.toxml(encoding='utf-8')
	
	out = open('template.%s.js.tmp' % language, 'w')

	for line in translated_expanded.split('\n'):
		escaped_line = escape_single_quote(line.strip())
		print >> out, "document.write('%s');" % escaped_line
	out.close()
	os.rename('template.%s.js.tmp' % language, 'template.%s.js' % language)



def main():
	# For each language, generate templated JS for it
	languages = [k for k in os.listdir('license_xsl/i18n/i18n_po/') if '.po' in k]
	
	languages = [re.split(r'[-.]', k)[1] for k in languages]
	for lang in languages:
		gen_templated_js(lang)

if __name__ == '__main__':
	main()
