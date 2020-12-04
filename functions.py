import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json
import glob
import multiprocessing
import re
from string import digits

#Gernating rules
def generate_rules(patterns, name):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    nlp.to_disk(name+"_ent_ruler")

def create_training_data(file, type):
    # data = generate_better_characters(file)
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    patterns = []
    for item in data:
        pattern = {
                    "label": type,
                    "pattern": item
                    }
        patterns.append(pattern)
    return (patterns)

def get_stopwords(file):
    with open (file, "r", encoding="utf-8") as f:
        stopwords = json.load(f)
    return (stopwords)

def get_sents(file):
    print (file)
    file = file.replace("\\", "/")
    stopwords = get_stopwords("data/stopwords.json")
    texts = []

    with open (file, "r", encoding="utf-8") as f:
        text = f.read().replace("\n", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    sents = text.split(".")
    print (len(sents))
    for sent in sents:
        sent = sent.replace("\n", " ").replace(":", "").replace(".", "").replace(",", "").replace("-", " ")
        sent = re.sub("[^A-Za-z']+", ' ', sent)
        words = sent.split(" ")
        for word in words:
            if word in stopwords:
                words.remove(word)
        new_words = []
        for word in words:
            word.strip()
            new_words.append(word)
        for word in new_words:
            if word.lower() in stopwords:
                new_words.remove(word)
        for word in new_words:
            if len(word) < 2:
                new_words.remove(word)
        if len(new_words) > 1:
            texts.append(new_words)

    output_file = file.replace(".txt", ".json")
    with open (output_file, "w") as f:
        json.dump(texts, f, indent=4)
    return (sents)

def json_data(files):
    all_data = []
    for file in files:
        file = file.replace("\\", "/")
        print (file)
        with open(file, "r") as f:
            data = json.load(f)
            for item in data:
                all_data.append(item)
    return (all_data)


def training(model_name):
    from gensim.models.word2vec import Word2Vec
    from gensim.models.phrases import Phrases, Phraser
    from collections import defaultdict
    import multiprocessing
    from gensim.models.keyedvectors import KeyedVectors
    from gensim.test.utils import common_texts, get_tmpfile
    with open ("data/corpus.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    print (len(texts))
    phrases = Phrases(texts, min_count=30, progress_per=10000)
    print ("Made Phrases")
    bigram = Phraser(phrases)
    print ("Made Bigrams")
    sentences = bigram[texts]
    print ("Found sentences")
    word_freq = defaultdict(int)

    for sent in sentences:
        for i in sent:
            word_freq[i]+=1

    print (len(word_freq))
    try:
        print (sorted(word_freq, key=word_freq.get, reverse=True)[:10])
    except:
        Exception
    print ("Training model now...")
    cores = multiprocessing.cpu_count()
    w2v_model = Word2Vec(min_count=1,
                        window=2,
                        size=500,
                        sample=6e-5,
                        alpha=0.03,
                        min_alpha=0.0007,
                        negative=20,
                        workers=cores-1)
    w2v_model.build_vocab(sentences, progress_per=10000)
    w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)
    with open(f"word_vectors/{model_name}.model","wb") as model_out:
        w2v_model.save(model_out)
    with open(f"word_vectors/word2vec_{model_name}.txt","wb") as w2v_out:
        w2v_model.wv.save_word2vec_format(w2v_out)

def testing(term):
    from gensim.models.word2vec import Word2Vec
    model = Word2Vec.load(f"word_vectors/word2vec_{model_name}.model")
    results = (model.wv.most_similar(positive=[term]))
    with open ("testing_results.txt", "a", encoding="utf-8") as f:
        for result in results:
            f.write(str(result)+"\n")

def train_rules_model(corpus, ent_ruler_model, output_file, prodigy=False):
    nlp=spacy.load(ent_ruler_model)
    TRAIN_DATA = []
    with open (corpus, "r", encoding="utf-8") as f:
        data = f.read()
        segments = data.split("\n")
        for segment in segments:
            segment = segment.strip()
            doc = nlp(segment)
            entities = []
            for ent in doc.ents:
                if prodigy==True:
                    entities.append({"start":ent.start_char, "end": ent.end_char,  "label": ent.label_})
                    pass
                else:
                    entities.append((ent.start_char, ent.end_char, ent.label_))
            if len(entities) > 0:
                if prodigy==True:
                    TRAIN_DATA.append({"text": segment, "spans": entities})
                else:
                    TRAIN_DATA.append([segment, {"entities": entities}])
    print (len(TRAIN_DATA))
    with open (output_file, "w", encoding="utf-8") as f:
        json.dump(TRAIN_DATA, f, indent=4)

def combine_patterns(labels):
    patterns = []
    for item in labels:
        data = create_training_data(item[0], item[1])
        for pattern in data:
            patterns.append(pattern)
    return (patterns)

def load_word_vectors(model_name):
    import subprocess
    import sys
    # spacy.init_model("en", "test")
    result = subprocess.run([sys.executable, "-m", "spacy", "init-model", "en", f"{model_name}", "--vectors-loc", f"word_vectors/word2vec_{model_name}.txt"])
    nlp = spacy.load(f"{model_name}")

def train_spacy(data, iterations, model_name):
    import random
    with open (data, "r", encoding="utf-8") as f:
        data = json.load(f)
    TRAIN_DATA = data
    print (len(TRAIN_DATA))
    nlp = spacy.load(model_name)
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            try:
                ner.add_label(ent[2])
            except:
                UnboundLocalError
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print ("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                            [text],
                            [annotations],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses
                )
            print (losses)
    nlp.to_disk(f"{model_name}")
    return (nlp)
