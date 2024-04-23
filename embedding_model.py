from sentence_transformers import SentenceTransformer


class EmbModel:
    def __init__(self, model_dir):
        self.model = SentenceTransformer(model_dir)

    def to_emb(self, sentence):
        if isinstance(sentence, str):
            sentence = [sentence]
        return self.model.encode(sentence)


if __name__ == '__main__':
    path = "D:/BaiduNetdiskDownload/Code/moka-ai_m3e-base"
    content = "2006年，Geoffrey Hinton提出通过逐层无监督预训练的方式来缓解由于梯度消失而导致的深层网络难以训练的问题，为神经网络的有效学习提供了重要的优化途径。"
    emb_model = EmbModel(path)
    emb = emb_model.to_emb(content)[0]
    print(emb)