from pymilvus import MilvusClient, CollectionSchema, FieldSchema, DataType
from pypinyin import lazy_pinyin
from embedding_model import EmbModel
from tqdm import tqdm


class EmbDatabase:
    def __init__(self, client, emb_dir, contents, name):
        self.client = client
        self.name = "_".join(lazy_pinyin(name))
        self.emb_model = EmbModel(emb_dir)

        if self.client.has_collection(self.name):
            self.client.drop_collection(self.name)

        if not self.client.has_collection(self.name):
            schema = CollectionSchema([
                FieldSchema("id", DataType.INT64, is_primary=True),
                FieldSchema("text", DataType.VARCHAR, max_length=2000),
                FieldSchema("emb", DataType.FLOAT_VECTOR, dim=self.emb_model.model.get_sentence_embedding_dimension())
            ])

            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name="emb",
                metric_type="COSINE",
                index_type="",
                index_name="vector_index"
            )

            self.client.create_collection(collection_name=self.name, schema=schema)
            self.client.create_index(self.name, index_params)

            for idx, content in tqdm(enumerate(contents), total=len(contents), desc=f"构建{name}向量库中"):
                emb = self.emb_model.to_emb(content)[0]
                client.insert(self.name, {"id": idx, "text": content, "emb": emb})

        self.client.load_collection(self.name)

    def search(self, content, topn=3):
        if isinstance(content, str):
            content = self.emb_model.to_emb(content)

        result = self.client.search(self.name,content,output_fields=["text"],limit=topn)
        _, _, t = zip(*[(d["id"], d["distance"], d["entity"]["text"]) for d in result[0]])

        return "".join(t)


if __name__ == '__main__':
    client = MilvusClient(uri="https://hz-t2.matpool.com:27863")
    emb_dir = "m3e-base"
    contents = ["牡丹鹦鹉又称为情侣鹦鹉、爱情鸟，是牡丹鹦鹉属内所有鹦鹉的总称", "分为三类，分别是1.费氏牡丹鹦鹉我们俗称：头类牡丹鹦鹉", "2.桃脸牡丹鹦鹉俗称：面类牡丹鹦鹉",
                "3.头类和面类的后代俗称：骡子。"]
    name = "牡丹鹦鹉"
    ques = "情侣鹦鹉、爱情鸟"
    emb_database = EmbDatabase(client, emb_dir, contents, name)
    ans = emb_database.search(ques)
    print(ans)