import gen_template_js

class thing_called_itself:
    def __init__(self, called):
        self.called = called
    def __repr__(self):
        return self.called

true = thing_called_itself('true')
false = thing_called_itself('false')

def get_contents(soup, attr):
    return str(soup(attr)[0].contents[0])

import BeautifulSoup
soup = BeautifulSoup.BeautifulStoneSoup(open('license_xsl/licenses.xml'))

ret = {}

def license_versions_for_jurisdiction(soup, in_juri):
    standard = soup('licenseclass', id='standard')[0]
    license2maxvers = {}
    for lic in standard('license'):
        lic_id = lic['id']
        for juri in lic('jurisdiction'):
            juri_id = juri['id']
            if juri_id == in_juri: # right jurisdiction
                for version in juri('version'):
                    version_id = version['id']
                    if license2maxvers.get(lic_id, '0') < version_id:
                        license2maxvers[lic_id] = version_id

    return license2maxvers

for j_i in soup('jurisdiction-info'):
    this_one = {}
    this_ones_id = str(j_i['id'])
    if this_ones_id:
        this_one['url'] = get_contents(j_i, 'uri')
        available_versions = license_versions_for_jurisdiction(soup=soup, in_juri=this_ones_id)
        if available_versions:
            this_one['version'] = str(max(available_versions.values()))
            
            if this_ones_id == '-':
                this_ones_id = 'generic'
                this_one['generic'] = true
            if this_ones_id == 'generic':
                name = 'Unported'
            else:
                name = gen_template_js.country_id2name(country_id=this_ones_id, language='en_US').encode("ascii")
            
            this_one['name'] = name
            ret[this_ones_id] = this_one

print ret

