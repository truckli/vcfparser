# vcfparser

A very simple Python 3 parser/formatter for vCard(vcf) files.

## example 1: load items from vCard files, and add attributes like phone numbers, organizations, job titles, et.al.
```python
import vcfparser

items = load('example.vcf')  
item = items['John Smith']
item.add_title('Superman') ## add a job title for this person
item.add_addr('A big house, U.S.A', 'HOME') ## add a home address for this person
item.add_org('A big company') ## add a home address for this person
item.add_phone('91115', 'Emergency') ## add a phone number 
print(item)
```

Output:

```
BEGIN:VCARD
VERSION:3.0
FN:John Smith
N:Smith;John;;;
TEL;TYPE=CELL:136
TEL;TYPE=WORK:011
ORG;CHARSET=UTF-8:A big company
ADR;TYPE=WORK;CHARSET=UTF-8:C502, Any Road
TITLE;CHARSET=UTF-8:Superman
ADR;TYPE=HOME;CHARSET=UTF-8:A big house, U.S.A
TEL;TYPE=Emergency:91115
END:VCARD
```


## example 2: construct an item from thin air
```python
import vcfparser

item = VcardItem()
item.construct("myname", 'mycell', 'myworkphone')
print(item)
```

Output:

```
BEGIN:VCARD
VERSION:3.0
FN:myname
N:myname;;;;
TEL;TYPE=CELL:mycell
TEL;TYPE=WORK:myworkphone
END:VCARD
```
