import base64
import tkinter
from pathlib import Path

from tkinter import filedialog


class Runner:
    encode_dir_name = "encode"
    decode_dir_name = "decode"

    __workspace = "D:/file-desensitization"

    def __init__(self):
        # 准备目录
        Path(self.__workspace).mkdir(exist_ok=True)
        Path(self.get_dir(Runner.encode_dir_name)).mkdir(exist_ok=True)
        Path(self.get_dir(Runner.decode_dir_name)).mkdir(exist_ok=True)

    def encode(self, file):
        content_bytes = file.read_bytes()
        encode_content = base64.b64encode(content_bytes)
        # 放到encode目录
        encode_file = self.get_dir(Runner.encode_dir_name) / (file.name + '.log')
        encode_file.write_text(str(encode_content, 'utf-8'))
        print("文件已保存至 %s" % encode_file)

    def decode(self, file):
        encode_content = file.read_text()
        decode_content = base64.b64decode(encode_content)
        # 放到decode目录
        decode_file = self.get_dir(Runner.decode_dir_name) / (file.name.replace(r'.log', ''))
        decode_file.write_bytes(decode_content)
        print("文件已保存至 %s" % decode_file)

    def get_dir(self, dir_name):
        return Path(self.__workspace) / dir_name

    @staticmethod
    def __get_file_list__(the_dir):
        file_list = []
        for entry in Path(the_dir).iterdir():
            if entry.is_file():
                file_list.append(entry)
        return file_list

    @staticmethod
    def pick_file():
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename()
        if file_path is None or file_path == '':
            return None
        return Path(file_path)


if __name__ == '__main__':
    print('------ 菜单 ------')
    print("[1] 文件加密")
    print("[2] 文件解密")
    action_code = input('输入序号选择功能:')

    runner = Runner()
    file = runner.pick_file()
    if file is None:
        print('未选择文件')
        input("按任意键结束程序...")
        exit()
    action_name = '加密' if '1' == action_code else '解密'
    print('开始%s文件[%s]' % (action_name, file))

    if '1' == action_code:
        runner.encode(file)
    else:
        runner.decode(file)
    input("按任意键结束程序...")
