import gradio as gr
import pandas as pd


def function1():
    pass


def function2():
    pass


def database_change():
    pass


def upload():
    pass


if __name__ == '__main__':
    database_namelist = ["1", "2", "3"]
    prompt_data = pd.read_excel("prompt.xlsx")
    input1 = gr.Dropdown(choices=database_namelist, label="知识库选择", value=database_namelist[0])
    input2 = gr.DataFrame(prompt_data, height=400)
    input3 = gr.UploadButton(label="上传知识库", file_count="directory")

    input4 = gr.Dropdown(choices=database_namelist, label="知识库选择", value=database_namelist[0])

    output1 = gr.Textbox(label="报告生成过程", lines=11, max_lines=14)
    output2 = gr.Textbox(label="报告生成内容", lines=11, max_lines=14)

    interface1 = gr.Interface(function1, [input1, input3, input2], [output1, output2], submit_btn="点击生成报告",
                              clear_btn=gr.Button("clear", visible=False), allow_flagging="never")
    interface2 = gr.Interface(function2, [input4, "text"], "text", allow_flagging="never")

    tab_interface = gr.TabbedInterface([interface1, interface2], ["报告生成", "知识库问答"], title="Report Generator😎")

    with tab_interface as tab_interface:
        input1.change(database_change, input1, input2)
        input3.upload(upload, input3, [input1, input2])
        tab_interface.launch(server_name="127.0.0.1", server_port=9999, show_api=False)
