import json


#####################################################################
#####################################################################
#####################################################################
#                         THE PRODIGY FORMAT                        #
{
  "text": "Apple updates its analytics service with new metrics",
  "spans": [{ "start": 0, "end": 5, "label": "ORG" }]
}
#####################################################################
#####################################################################
#####################################################################

def convert(spacy_file, prodigy_file):
    with open (spacy_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        NEW = []
        for item in data:
            text = (item[0])
            all_data = {"text": text}
            entities = []
            for ent in item[1]["entities"]:
                entity = {"start": ent[0], "end": ent[1], "label": ent[2]}
                entities.append(entity)
            all_data["spans"] = entities
            NEW.append(all_data)
    with open (prodigy_file, "w", encoding="utf-8") as f:
        json.dump(NEW, f, indent=4)

convert("data/TRAIN_DATA.json","data/smithsonian_ner.json")
