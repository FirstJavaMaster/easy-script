import os
import re
import winreg

# 存档中世界的名字
import psutil

world_name = 'Cluster_1'
# steamCMD的安装目录
steam_dir = r'E:/SteamCMD'

# steamCMD可执行文件的名称
steam_exe_name = 'dontstarve_dedicated_server_nullrenderer.exe'

# 版本号
version = 1.0


# 获取游戏存档目录
def get_save_file_dir():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    document_dir = winreg.QueryValueEx(key, 'Personal')[0]
    return '%s/Klei/DoNotStarveTogether/%s' % (document_dir, world_name)


def get_game_home():
    return steam_dir + "/steamapps/common/Don't Starve Together Dedicated Server"


class Game:
    @staticmethod
    def update_game():
        print('开始检查更新...')
        command = '%s/steamcmd.exe +login anonymous +app_update 343050 validate +quit' % steam_dir
        os.system(command)

    @staticmethod
    def stop():
        if Game.status():
            print('关闭正在运行的服务器')
            os.system('taskkill /F /IM %s' % steam_exe_name)

    @staticmethod
    def start():
        exe_dir = get_game_home() + "/bin"
        os.chdir(exe_dir)
        os.system('start "DST Master" %s -console -cluster %s -shard Master' % (steam_exe_name, world_name))
        os.system('start "DST Caves" %s -console -cluster %s -shard Caves' % (steam_exe_name, world_name))

    @staticmethod
    def restart():
        Game.stop()
        Game.start()

    @staticmethod
    def status():
        pid_list = psutil.pids()
        active = False
        for pid in pid_list:
            p = psutil.Process(pid)
            if p.name() == steam_exe_name:
                print('找到进程 %s -- %s' % (pid, p.name()))
                active = True
        if not active:
            print('服务未运行')
        return active


class Mod:
    @staticmethod
    def get_mod_id_list():
        print('获取mod列表 ...')
        mod_setting_file_path = get_save_file_dir() + '/Master/modoverrides.lua'
        with open(mod_setting_file_path, 'r') as mod_file:
            content = mod_file.read()
            result = re.findall(r'workshop-(\d+)+', content)

            print(result)
            return result

    @staticmethod
    def write_to_download_setting_file(mod_id_list):
        file_path = "%s/steamapps/common/Don't Starve Together Dedicated Server/mods/dedicated_server_mods_setup.lua" % steam_dir
        print('将mod列表写入下载配置文件 %s ...' % file_path)
        with open(file_path, 'a+') as file:
            file.write('\n\n')
            for mod_id in mod_id_list:
                file.write('\tServerModSetup("%s")\n' % mod_id)
            file.close()
        print('写入完毕')

    @staticmethod
    def update_mod():
        # 获取mod列表
        mod_id_list = Mod.get_mod_id_list()
        # 写入文件
        Mod.write_to_download_setting_file(mod_id_list)


def menu():
    print()
    print('饥荒联机工具 v%s' % version)
    print('  1. 更新游戏')
    print('  2. 刷新mod配置')
    print('  3. 查看服务状态')
    print('  4. 启动服务')
    print('  5. 停止服务')
    print('  6. 重启服务')
    print()
    input_value = input('输入数字, 选择功能. 输入回车退出程序 >>> ')

    print()
    if input_value == '':
        print('程序退出')
        return False

    if input_value == '1':
        Game.stop()
        Game.update_game()
        Mod.update_mod()
    elif input_value == '2':
        Mod.update_mod()
    elif input_value == '3':
        Game.status()
    elif input_value == '4':
        Game.start()
    elif input_value == '5':
        Game.stop()
    elif input_value == '6':
        Game.restart()
    else:
        print('!!! 输入有误, 请重新输入 !!!')
    return True


if __name__ == '__main__':
    while True:
        try:
            result = menu()
            if not result:
                break
        except Exception as ex:
            print(ex)
            menu()
