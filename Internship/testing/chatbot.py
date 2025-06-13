import spacy
import numpy as np
nlp = spacy.load("en_core_web_md")
txt = "gi gi gi gi"
vector = nlp(txt).vector
print("Embedding shape:" , vector.shape)
print("vector value", vector[:5])

def cosine_similarity(vec1,vec2):
    return np.dot(vec1,vec2 )/ (np.linalg.norm(vec1) * np.linalg.norm(vec2))

query1 = nlp("How do I change my password?").vector
query2 = nlp("How do I reset my password?").vector

similarity = cosine_similarity(query1, query2)
print("Similarity score:", similarity)
