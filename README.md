# vcfparser

A very simple Python 3 parser for vCard(vcf) files.



## example 1: load items from vCard files
```python
items = load('example.vcf')  
item = items['John Smith']
item.add_title('Superman') ## add a job title for this person
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
ORG;CHARSET=UTF-8:Any Org
ADR;TYPE=WORK;CHARSET=UTF-8:C502, Any Road
TITLE;CHARSET=UTF-8:Superman
END:VCARD
```


## example 2: construct an item from thin air
```python
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
