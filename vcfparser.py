#!/usr/bin/env python
# #-*- coding=utf-8 -*-

import re
import codecs

class VcardItem():
    def __init__(self, text = ''):
        self.text = text
        self.kv = {}
        self.main_kv = {}
        self.version = '3.0'
        self.fn = None
        self.is_modified = False
        if text == '':
            self.is_modified = True
        else:
            self.loads(text)
        
    def loads(self, text):
        self.text = text
        for m in re.finditer(r"(.*?)\r\n(?!\s)", text, re.MULTILINE|re.DOTALL):
            line = m.group(1)
            if line.find(':') < 0: continue
            key = line.split(':')[0]
            value = line[len(key)+1:]
            key = key.upper()
            if key in {'BEGIN','END'}: continue
            if key == 'VERSION':
                self.version = value
            elif key == 'FN':
                self.fn = value
            elif key.startswith("TEL;TYPE=CELL"):
                self.add_phone(value,'CELL')
            elif key.startswith("TEL;TYPE=WORK"):
                self.add_phone(value,'WORK')
            elif key.startswith("ORG;") or key.startswith("ORG:"):
                self.main_kv[key] = value
            elif key.startswith("ADR;") or key.startswith("ADR:"):
                self.main_kv[key] = value
            elif key.startswith("TITLE;") or key.startswith("TITLE:"):
                self.main_kv[key] = value
            else:
                self.kv[key] = value
    
    ### search by text content
    def search_value(self, value):
        results = {}
        for key in self.main_kv:
            if self.main_kv[key].find(value) >= 0:
                results[key] = self.main_kv[key]
        for key in self.kv:
            if self.kv[key].find(value) >= 0:
                results[key] = self.kv[key]
        return results
    
    def add_phone(self, value, type='CELL'):
        self.is_modified = True
        key = "TEL;TYPE=" + type
        value = value.replace(' ', '')# not allow spaces in phone nums
        self.main_kv[key] = value ## not allows duplicates in phone types
    
    def add_addr(self, value, addr_type='HOME'):
        self.is_modified = True
        key = "ADR;TYPE=%s;CHARSET=UTF-8" % (addr_type)
        self.main_kv[key] = value
        
    def add_org(self, value):
        self.is_modified = True
        key = "ORG;CHARSET=UTF-8"
        self.main_kv[key] = value
    
    def add_title(self, value):
        self.is_modified = True
        key = "TITLE;CHARSET=UTF-8"
        self.main_kv[key] = value
    
    def del_key(self, key):
        if key in self.kv:
            del self.kv[key]
            self.is_modified = True
        if key in self.main_kv:
            del self.main_kv[key]
            self.is_modified = True
        
        
    def construct(self, name, cellphone=None, workphone=None, org=None, title=None, work_addr=None, home_addr=None):
        if name is None or len(name) == 0: 
            return
        self.fn = name
        self.is_modified = True
        if len(name) <= 3 and re.search("[A-Za-z0-9]", name) is None:
            name = "%s;%s;;;" % (name[0], name[1:])
        else:
            name += ";;;;"
        self.kv['N'] = name
        if cellphone is not None:
            self.add_phone(cellphone, 'CELL')
        if workphone is not None:
            self.add_phone(workphone, 'WORK')
        if org is not None:
            self.add_org(org)
        if title is not None:
            self.add_title(title)
        if work_addr is not None:
            self.add_addr(work_addr, 'WORK')
        if home_addr is not None:
            self.add_addr(home_addr, 'HOME')
    
    def show(self):
        if not self.is_modified: return str(self.text)
        text = "BEGIN:VCARD\r\nVERSION:%s\r\nFN:%s\r\n" % (self.version, self.fn)
        for key in self.kv:
            text += "%s:%s\r\n" % (key, self.kv[key])
        for key in self.main_kv:
            text += "%s:%s\r\n" % (key, self.main_kv[key])
        text += "END:VCARD\r\n"
        return text
    
    def __str__(self):
        return self.show()
      
def load(fname):
    content = codecs.open(fname, "r", "utf-8").read()
    items = {} 
    item_pattern = re.compile(r"^BEGIN:VCARD.*?^END:VCARD", re.MULTILINE|re.DOTALL)
    for m in re.finditer(item_pattern, content):
        vi = VcardItem(m.group(0))
        items[vi.fn] = vi
    return items

'''
## example 1: load items from vCard files
items = load('example.vcf')  
item = items['John Smith']
item.add_title('Superman') ## add a job title for this person
print(item)

## example 2: construct an item from thin air
item = VcardItem()
item.construct("myname", 'mycell', 'myworkphone')
print(item)
'''



