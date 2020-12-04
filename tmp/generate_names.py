titles = ["Mr.", "Mr ", "Dr.", "Dr.", "Mrs.", "Mrs", "Miss", "Ms."]

# import json
# last_names = []
# with open ("tmp/people.json", "r", encoding="utf-8") as f:
#     names = json.load(f)
#     for name in names:
#         if len(name) > 3:
#             last_names.append(name)
# print (len(last_names))
#
# first_names = []
# with open ("tmp/female_firstnames.json", "r", encoding="utf-8") as f:
#     names = json.load(f)
#     for name in names:
#         if len(name) > 3:
#             first_names.append(name)
#
# with open ("tmp/male_firstnames.json", "r", encoding="utf-8") as f:
#     names = json.load(f)
#     for name in names:
#         if len(name) > 3:
#             first_names.append(name)
import re
import json
with open ("data/corpus.txt", "r", encoding="utf-8") as f:
    corpus = f.read()

spouses = re.findall(r"(?:[M|D|M]r[.]? and Mrs[.]?) \b[A-Z].*?\b[A-Z][a-z].*?\b", corpus)
spouses2 = re.findall(r"(?:[M|D|M]r[.]? and Mrs[.] [A-Z]. [A-Z]. [A-Za-z]+)", corpus)
spouses3 = re.findall(r"(?:[M|D|M]r[.]? and Mrs[.] [A-Z]. [A-Z]. [A-Z]. [A-Za-z]+)", corpus)

# combined = spouses+spouses2
# final = []
# combined = list(set(combined))
# for name in combined:
#     if len(name) < 100:
#         final.append(name)

to_delete = []
text = " ".join(spouses)
print (len(spouses))
for spouse in spouses2:
    if spouse[0:17] in text:
        to_delete.append (spouse[0:17])
        print (spouse[0:17])
for item in to_delete:
    for spouse in spouses:
        if item in spouse:
            try:
                spouses.remove(spouse)
            except:
                Exception
print (len(spouses))



to_delete = []
text = " ".join(spouses2)
for spouse in spouses3:
    if spouse[0:20] in text:
        to_delete.append (spouse[0:20])
        print (spouse[0:20])
print (len(spouses2))
for item in to_delete:
    for spouse in spouses2:
        if item in spouse:
            spouses2.remove(spouse)
print (len(spouses2))

total = spouses+spouses2+spouses3
all_names = []
for item in total:
    if len(item) < 50:
        all_names.append(item)

# with open ("data/spouses.json", "w", encoding="utf-8") as f:
#     json.dump(all_names, f, indent=4)
