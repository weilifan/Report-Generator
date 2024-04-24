import os
from embedding_model import EmbModel
import faiss
import pickle


class EmbDatabase:
    def __init__(self, emb_dir, contents, name):
        self.emb_model = EmbModel(emb_dir)

        if not os.path.exists(os.path.join(".cache", f"{name}_faiss_index.pkl")):
            index = faiss.IndexFlatL2(self.emb_model.model.get_sentence_embedding_dimension())
            embs = self.emb_model.to_emb(contents)
            index.add(embs)

            with open(os.path.join(".cache",f"{name}_faiss_index.pkl"),"wb") as f:
                pickle.dump(index,f)
        else:
            with open(os.path.join(".cache",f"{name}_faiss_index.pkl"),"rb") as f:
                index = pickle.load(f)
        self.index = index
        self.contents = contents

    def add(self, emb):
        self.index.add(emb)

    def search(self, content, topn=3):
        if isinstance(content,str):
            content = self.emb_model.to_emb(content)

        distances, idxs = self.index.search(content, topn) # mlivus

        results = [self.contents[i] for i in idxs[0]]
        return results


if __name__ == '__main__':
    emb_dir = "m3e-base"
    contents = ["牡丹鹦鹉又称为情侣鹦鹉、爱情鸟，是牡丹鹦鹉属内所有鹦鹉的总称", "分为三类，分别是1.费氏牡丹鹦鹉我们俗称：头类牡丹鹦鹉", "2.桃脸牡丹鹦鹉俗称：面类牡丹鹦鹉", "3.头类和面类的后代俗称：骡子。"]
    name = "牡丹鹦鹉"
    ques = "情侣鹦鹉、爱情鸟"
    emb_database = EmbDatabase(emb_dir, contents, name)
    ans = emb_database.search(ques)
    print(ans)