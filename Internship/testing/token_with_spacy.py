import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp( "hi how are you doing")
txt = nlp("Hi my dog is very fast and is rainbow in color")

for i in txt:    #POS tagging
    print(f"{i.text}:{i.pos_} ({i.tag_})")

for ent in txt.ents:    #Exyracted entities name
    print(f"{ent.text} → {ent.label_} ({spacy.explain(ent.label_)})")

for token in txt:    #perferform dependency parsing
    print(f"{token.text}: {token.dep_} → Head: {token.head.text}")