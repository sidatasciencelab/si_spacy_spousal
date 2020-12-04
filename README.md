# SI spaCy Spousal NER Model

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sidatasciencelab/si_spacy_spousal/master)

From William's description in Slack:

The smithsonian_domain model is pretrained to recognize and extract SPOUSAL 
entities only. It's not what I would call SOTA, but it's enough to use the 
ner.correct recipe in Prodigy to speed up the annotation of a gold training set.

I included all the extra functions I've been writing the past few days in that 
folder as well under functions.py . The demo.py shows you how to use it. The 
patterns I created were based on regex rules that I passed to the EntityRuler 
in spaCy that then cultivated a good training set based on known patterns of 
250 or so paragraphs. It then trained a spaCy ML NER model on that training set. 
You can include PERSON tags easily as well if you get a list of personal names. 
I believe the spaCy entity ruler if it finds 2 patterns that match, it defaults 
to the longer one's label, so that should keep SPOUSAL tags separate from PERSON 
tags.
