from gensim.models.doc2vec import TaggedDocument
from gensim.utils import simple_preprocess as preprocess
from gensim.models import Doc2Vec
import numpy as np
import csv


def doc2vec():
    with open("items.txt", "r") as f:
        render = csv.reader(f, delimiter="\t")

        train_corpus = [
            TaggedDocument(preprocess(row[3]), [i])
            for i, row in enumerate(render)
        ]
        
    model = Doc2Vec(vector_size=50)
    model.build_vocab(train_corpus)

    model.train(train_corpus, total_examples=model.corpus_count, epochs=100)

    model.save("items.model")
    
    vecs = []
    with open("items.txt", "r") as f:
        render = csv.reader(f, delimiter="\t")
        for row in render:
            vecs.append(model.infer_vector(row[3]))
    
    np.save("vecs.npy", np.array(vecs))

    sim = cos_sim(vecs, vecs)

    ranks = []
    scores = []
    for i in range(len(sim)):
        ranks.append(np.argsort(sim[i])[::-1][1:11])
        scores.append(np.sort(sim[i])[::-1][1:11])


def cos_sim(x, y, eps=1e-8):
  nx = x / ((np.sqrt(np.sum(x ** 2, axis=1) + eps)).reshape(-1, 1))
  ny = y / ((np.sqrt(np.sum(y ** 2, axis=1) + eps)).reshape(-1, 1))
  return np.dot(nx, ny.T)


if __name__ == "__main__":
    doc2vec()