import base64

from runner import Runner

runner = Runner()
file = runner.pick_file()
if file is None:
    print('未选择文件')
    input("按任意键结束程序...")
    exit()

encode_content = file.read_text()
decode_content = base64.b64decode(encode_content)
# 放到decode目录
decode_file = runner.get_dir(Runner.decode_dir_name) / (file.name.replace(r'.log', ''))
print("文件即将保存至 %s" % decode_file)
input("按任意键继续...")

decode_file.write_bytes(decode_content)
print("文件已保存至 %s" % decode_file)
input("按任意键结束程序...")
