import gradio as gr
import pandas as pd
import os
import shutil
import jieba.analyse as aly
from collections import Counter
from database_creator import DatabaseCreator
from chat_model import ChatModel


class Interface:
    def __init__(self, dir_path, api_key):
        self.dir_path = dir_path
        self.database_list = []
        self.database_namelist = []
        self.chat = ChatModel(api_key=api_key)

        dirs = [name for name in os.listdir(self.dir_path) if os.path.isdir(f"{self.dir_path}/{name}")]

        for dir in dirs:
            database = DatabaseCreator(f"{self.dir_path}/{dir}", dir)

            self.database_list.append(database)
            self.database_namelist.append(dir)

    def report_generation(self, name, input3, input2):
        database = self.database_list[database_namelist.index(name)]

        result1 = []
        result2 = []

        result1.append("内容解析中......")
        yield "\n".join(result1), "\n".join(result2)

        all_report = ""
        for p_n, group in database.prompt_data.groupby("段落"):
            result1.append(f"第{p_n}段内容生成中......")

            yield "\n".join(result1), "\n".join(result2)

            p_n_content = []
            for question in group["prompt"]:
                search_result = database.search(question, 3)

                search_result = "\n".join(search_result)

                prompt = f"请根据已知内容简洁明了的回复用户的问题，已知内容如下：```{search_result}```,用户的问题是：{question}，如何已知内容无法回答用户的问题，请直接回复：不知道，无需输出其他内容"

                response = self.chat.get_ans(prompt)
                result1.append("检索及回答内容:\n")
                for trunk in response:
                    result1[-1] += trunk.choices[0].delta.content
                    yield "\n".join(result1), "\n".join(result2)

                result1[-1] = result1[-1].replace("\n", "")
                p_n_content.append(result1[-1])

                result1.append("*" * 30)
                yield "\n".join(result1), "\n".join(result2)

            prompt_report = f"你是一个大学教授，你需要根据相关内容，来撰写一段内容，生成的结果必须严格来自相关内容，语言必须严谨、符合事实，不能使用第一人称，相关内容如下：\n```\n{''.join(p_n_content)}\n```\n生成的结果为："

            result1.append("第一段报告内容:\n")
            result2.append("\t\t\t")
            yield "\n".join(result1), "\n".join(result2)

            response = self.chat.get_ans(prompt_report)

            for trunk in response:
                result1[-1] += trunk.choices[0].delta.content
                result2[-1] += trunk.choices[0].delta.content

                result1[-1] = result1[-1].replace("\n", "")
                result2[-1] = result2[-1].replace("\n", "")
                yield "\n".join(result1), "\n".join(result2)

            all_report += result2[-1]
            all_report += "\n"

            result1.append("*" * 30)
            yield "\n".join(result1), "\n".join(result2)

    def question_answering(self, name, text):
        database = self.database_list[database_namelist.index(name)]

        result = [""]

        search_result = database.search(text, 3)
        search_result = "\n".join(search_result)

        prompt = f"请根据已知内容简洁明了的回复用户的问题，已知内容如下：```{search_result}```,用户的问题是：{text}，如何已知内容无法回答用户的问题，请直接回复：不知道，无需输出其他内容"

        response = self.chat.get_ans(prompt)

        for trunk in response:
            result[-1] += trunk.choices[0].delta.content
            yield "\n".join(result)

    def database_change(self, name):
        return self.database_list[database_namelist.index(name)].prompt_data

    def upload(self, files):
        check_txt = False
        check_prompt_xlsx = False

        for file in files:
            if check_txt and check_prompt_xlsx:
                break
            if file.name.endswith(".txt"):
                check_txt = True
            elif file.name.endswith("prompt.xlsx"):
                check_prompt_xlsx = True
        else:
            if not check_txt:
                raise Exception("请上传包含txt文档的文件夹")
            if not check_prompt_xlsx:
                raise Exception("请上传包含prompt.xlsx的文件夹")

        content = []
        for file in files:
            try:
                with open(file.name, encoding="utf-8") as f:
                    data = f.readlines(1)
                    content.extend(aly.tfidf(data[0]))
            except:
                continue
        count = Counter(content)
        kw = count.most_common(2)
        type_name = "".join([i[0] for i in kw])

        save_path = os.path.join(self.dir_path, type_name)

        if not os.path.exists(save_path):
            os.mkdir(save_path)
            os.mkdir(os.path.join(save_path, "txt"))
        for file in files:
            if file.name.endswith(".txt"):
                shutil.copy(file.name, os.path.join(save_path, "txt"))
            elif file.name.endswith("prompt.xlsx"):
                shutil.copy(file.name, save_path)

        database = DatabaseCreator(save_path, type_name)
        self.database_list.append(database)
        database_namelist.append(type_name)
        input1.choices.append((type_name, type_name))

        return type_name, database.prompt_data


if __name__ == '__main__':
    dir_path = "database"
    zhipu_key = ""  # 在此处粘贴智谱AI的key
    dirs = [name for name in os.listdir(dir_path) if os.path.isdir(f"{dir_path}/{name}")]

    database_list = []
    database_namelist = []

    for dir in dirs:
        database = DatabaseCreator(f"{dir_path}/{dir}", dir)

        database_list.append(database)
        database_namelist.append(dir)

    input1 = gr.Dropdown(choices=database_namelist, label="知识库选择", value=database_namelist[0])
    input2 = gr.DataFrame(database_list[0].prompt_data,
                          height=400,
                          label="报告大纲",
                          interactive=False
                          )
    input3 = gr.UploadButton(label="上传知识库", file_count="directory")

    input4 = gr.Dropdown(choices=database_namelist, label="知识库选择", value=database_namelist[0])

    input5 = gr.Textbox(label="请输入问题")

    output1 = gr.Textbox(label="报告生成过程", lines=11, max_lines=14)
    output2 = gr.Textbox(label="报告生成内容", lines=11, max_lines=14)
    output3 = gr.Textbox(label="答案")

    functions = Interface(dir_path=dir_path, api_key=zhipu_key)

    interface1 = gr.Interface(functions.report_generation, [input1, input3, input2], [output1, output2],
                              submit_btn="生成报告",
                              clear_btn=gr.Button("clear", visible=False),
                              allow_flagging="never")
    interface2 = gr.Interface(functions.question_answering, [input4, input5], output3,
                              submit_btn="生成答案",
                              clear_btn=gr.Button("clear", visible=False),
                              allow_flagging="never")

    tab_interface = gr.TabbedInterface([interface1, interface2], ["报告生成", "知识库问答"], title="😎")

    with tab_interface as tab_interface:
        input1.change(functions.database_change, input1, input2)
        input3.upload(functions.upload, input3, [input1, input2])
        tab_interface.queue().launch(server_name="127.0.0.1", server_port=9996, show_api=False)
