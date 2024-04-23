import os
import pickle
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter


class TextSplitter:
    def __init__(self, dir, name):
        loader = DirectoryLoader(dir)
        documents = loader.load()
        if not os.path.exists(os.path.join(".cache", f"{name}_contents.pkl")):
            text_spliter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)

            split_docs = text_spliter.split_documents(documents)
            contents = [i.page_content for i in split_docs]
            with open(os.path.join(".cache", f"{name}_contents.pkl"), "wb") as f:
                pickle.dump(contents, f)
        else:
            with open(os.path.join(".cache", f"{name}_contents.pkl"), "rb") as f:
                contents = pickle.load(f)
        self.contents = contents


if __name__ == '__main__':
    dir = "D:/BaiduNetdiskDownload/Code/database1/txt"
    name = "小米汽车"
    text_spliter = TextSplitter(dir, name)
    print(text_spliter.contents)