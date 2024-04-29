1. 功能
    - 根据不同的知识库和段落大纲，自动生成文档
      - ![img](https://github.com/weilifan/Report-Generator/blob/master/demo/report_generation.gif)
    - 根据不同知识库回答问题
      - ![img](https://github.com/weilifan/Report-Generator/blob/master/demo/question_answering.gif)
    - 上传新的知识库并在不同知识库之间切换
      - ![img](https://github.com/weilifan/Report-Generator/blob/master/demo/data_uploading.gif)
    - 上传新的知识库时，也可以直接把文件夹放在database下
      - 参考文件需要是txt格式。文件夹中还需要包含一个xlsx大纲文件。 
      - 不对知识库文件夹名称做规定，本程序会使用自动在文档中提取关键词来给知识库命名 
      - 如果上传的文件夹名称提取出的关键词为已存在知识库，那么会在已存在知识库中追加写入
2. 部署和使用
    - 安装`requirements.txt`中的所有依赖
    - 将智谱AI的key放在`main.py`的`zhipu_key = "key"`中，申请智谱AI的key：`https://open.bigmodel.cn/usercenter/apikeys`
    - 为了使用langchain chunk做文档分割，需要将mltk_data依赖包放在环境的lib中（例如：`D:\Miniconda3\envs\env_pytorch\Lib`） 
    - 向量数据库默认使用faiss构建，如果要使用milvus向量数据库，
      - 在`database_creator.py`中将milvus注释部分取消
      - 使用docker在服务器上启动milvus向量数据库（以ubuntu 18.04服务器为例）
        - 开放19530端口，一定要开放19530端口，否则链接不上
        - docker安装: 可参考`https://docs.docker.com/desktop/install/ubuntu/`, `https://blog.csdn.net/x7536987/article/details/124808845`
        - docker compose安装: 可参考`https://docs.docker.com/compose/install/standalone/`, `https://blog.csdn.net/k393393/article/details/122926513`
        - 在服务器上安装并启动milvus: 可参考`https://milvus.io/docs/install_standalone-docker-compose.md`
      - 将该服务器的公网填写在`database_creator.py`中的`uri = "http://服务器公网:19530"`

