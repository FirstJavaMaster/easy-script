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
    Runner.pick_file()
