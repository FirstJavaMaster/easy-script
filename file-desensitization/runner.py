import base64
import os
from pathlib import Path


def __encode__():
    file_list = __get_file_list__(__get_source_dir__())
    for file in file_list:
        content_bytes = file.read_bytes()
        encode_content = base64.b64encode(content_bytes)
        # 放到encode目录
        encode_file = Path(__get_encode_dir__()) / file.name
        encode_file.write_text(str(encode_content, 'utf-8'))


def __decode__():
    file_list = __get_file_list__(__get_encode_dir__())
    for file in file_list:
        encode_content = file.read_text()
        decode_content = base64.b64decode(encode_content)
        # 放到decode目录
        decode_file = Path(__get_decode_dir__()) / file.name
        decode_file.write_bytes(decode_content)


def __get_file_list__(dir):
    file_list = []
    for entry in Path(dir).iterdir():
        if entry.is_file():
            file_list.append(entry)
    return file_list


def __get_source_dir__():
    return os.path.join(__get_workspace__(), "source")


def __get_encode_dir__():
    return os.path.join(__get_workspace__(), "encode")


def __get_decode_dir__():
    return os.path.join(__get_workspace__(), "decode")


def __get_workspace__():
    return os.path.split(os.path.realpath(__file__))[0]


if __name__ == '__main__':
    # 准备目录
    Path(__get_encode_dir__()).mkdir(exist_ok=True)
    Path(__get_decode_dir__()).mkdir(exist_ok=True)
    #
    __encode__()
    __decode__()
