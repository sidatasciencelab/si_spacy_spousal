import spacy

with open ("data/corpus.txt", "r", encoding="utf-8") as f:
    text = f.read().replace("\n", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text[0:1000000]

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
sentences = []
for sent in doc.sents:
    sentences.append(str(sent))
    if "Mr. and Mrs." in sent.text:
        print (sent.text)

results = []
nlp = spacy.load("smithsonian_domain")
for sent in sentences:
    doc = nlp(sent)
    for ent in doc.ents:
        results.append((sent, (ent.text, ent.label_)))

import json
with open ("tmp/results_2.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)
