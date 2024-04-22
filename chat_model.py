from zhipuai import ZhipuAI


class ChatModel:
    def __init__(self, api_key):
        self.client = ZhipuAI(api_key=api_key)

    def get_ans(self, prompt):
        response = self.client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            top_p=0.3,
            temperature=0.45,
            max_tokens=1024,
            stream=True,
        )
        return response


if __name__ == '__main__':
    key = ""  # 在此处粘贴智谱AI的key
    ques = "你好"
    chat_model = ChatModel(key)
    ans = chat_model.get_ans(ques)
    print(ans)