import functions

### DATA ###
model_name = "smithsonian_domain"
labeled_data = [("data/spouses.json", "SPOUSAL")]


### CREATING SPACY ENTITY RULER ###
#generate the patterns based on labeled_data
# patterns = functions.combine_patterns(labels=labeled_data)

#passes those patterns to a blank spacy model EntityRuler
# functions.generate_rules(patterns, name=model_name)

#using generated entity ruler to create a training set for spacy model
# functions.train_rules_model("data/corpus.txt", f"{model_name}_ent_ruler", "data/TRAIN_DATA.json")


### WORD VECTORS ###
#Generates sentences without stopwords for training Gensim Model
# sents = functions.get_sents("data/corpus.txt")

#generates Gensim word2vec model and outputs the word vectors
# functions.training(model_name=model_name)


### CREATING SPACY NER MODEL, INJECTING WORD VECTORS, TRAINING ON THE TRAIN_DATA ###
#loads the word vectors into a blank spaCy model and saves it
# functions.load_word_vectors(model_name)

#creates and trains the NER model in the newly created spaCy model with the word vectors
functions.train_spacy("data/TRAIN_DATA.json", 10, model_name)
