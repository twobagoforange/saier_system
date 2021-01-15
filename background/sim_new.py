from gensim import corpora, models, similarities, utils
import jieba
import heapq
import numpy as np


def get_sim_top10(new_doc):
    try:
        documents = np.load('Saier/document.npy').tolist()
        print(documents)
    except Exception as e:
        print(e)
    dictionary = corpora.Dictionary.load('Saier/dictionary.dict')
    tfidf = models.TfidfModel.load("Saier/tfidf.model")
    index = similarities.MatrixSimilarity.load('Saier/document_index.index')

    words = ' '.join(jieba.cut(new_doc)).split(' ')
    new_text = []
    for word in words:
        new_text.append(word)

    new_vec = dictionary.doc2bow(new_text)
    new_vec_tfidf = tfidf[new_vec]

    sims = index[new_vec_tfidf]
    sims_list = sims.tolist()
    top10 = heapq.nlargest(10, sims_list)
    res_list = []
    for i in top10:
        res_list.append(documents[sims_list.index(i)].strip())
    return res_list


if __name__ == "__main__":
    get_sim_top10("直接寻址是寻址方式。")
