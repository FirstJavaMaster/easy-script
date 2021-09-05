import base64

from runner import Runner

runner = Runner()
file = runner.pick_file()
if file is None:
    print('未选择文件')
    input("按任意键结束程序...")
    exit()

content_bytes = file.read_bytes()
encode_content = base64.b64encode(content_bytes)
# 放到encode目录
encode_file = runner.get_dir(Runner.encode_dir_name) / (file.name + '.log')
print("文件即将保存至 %s" % encode_file)
input("按任意键继续...")

encode_file.write_text(str(encode_content, 'utf-8'))
print("文件已保存至 %s" % encode_file)
input("按任意键结束程序...")
