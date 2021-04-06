import datetime
import os
import shutil
from pathlib import Path

# 缓存文件名
temp_file_name = 'last_ip.txt'


# 检查上一次的ip, 返回True说明有更新, 否则返回False
def check_ip_change(ip):
    temp_file = Path(temp_file_name)
    # 文件不存在
    if not temp_file.exists():
        print('cache不存在. 新建cache.')
        return update_cache(ip)
    # 是文件夹
    if temp_file.is_dir():
        print('cache是文件夹. 删除并新建cache.')
        shutil.rmtree(temp_file_name)
        return update_cache(ip)
    # 文件存在则比较内容, 如果比较结果是 IP未变且更新时间小于设置间隔 则认为不需发送邮件
    with open(temp_file_name, 'r') as f:
        last_ip = f.read()
        file_m_time = datetime.datetime.fromtimestamp(os.path.getmtime(temp_file_name))
        print('读取cache. IP [%s] 最后更新时间 [%s]' % (last_ip, file_m_time))
        # 如果ip变了, 则删除文件
        if last_ip != ip:
            print('ip发生变化(%s --> %s). 刷新cache.' % (last_ip, ip))
            return update_cache(ip)
        # 如果ip没变
        if file_m_time + datetime.timedelta(hours=2) < datetime.datetime.now():
            print('超出预设时间. 刷新cache')
            return update_cache(ip)
        # ip没变, 且未"超时", 不做处理
        print('ip没变, 且未超时, 不做处理')
        return IpCacheCheckResult(False, last_ip, file_m_time)


def update_cache(ip):
    print('更新IP记录: %s' % ip)
    with open(temp_file_name, 'w+') as f:
        f.write(ip)
    return IpCacheCheckResult(True, ip, datetime.datetime.now())


class IpCacheCheckResult:
    result = None
    last_ip = None
    last_m_time = None

    def __init__(self, result, last_ip, last_m_time):
        self.result = result
        self.last_ip = last_ip
        self.last_m_time = last_m_time


if __name__ == '__main__':
    result = check_ip_change('123')
    print(result)
