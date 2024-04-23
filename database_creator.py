import os
import pandas as pd
from text_spliter import TextSplitter
from embedding_database import EmbDatabase


class DatabaseCreator:
    def __init__(self, path, name=None):
        if name is None:
            name = path

        if not os.path.exists(os.path.join(path, "txt")):
            print("对应的知识库txt文件夹不存在")
            exit(-999)
        if not os.path.exists(os.path.join(path, "prompt.xlsx")):
            print("prompt模板不存在")
            exit(-998)
        if not os.path.exists(".cache"):
            os.mkdir(".cache")

        self.prompt_data = pd.read_excel(os.path.join(path, "prompt.xlsx"))
        self.document = TextSplitter(os.path.join(path, "txt"), name)
        self.emb_database = EmbDatabase("m3e-base", self.document.contents, name)

    def search(self, text, topn=3):
        return self.emb_database.search(text, topn)