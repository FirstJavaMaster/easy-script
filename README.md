"# script" 

## 自动备份数据库脚本

在服务器上进入你想要放置脚本的目录，如：

    cd /opt/jobs

从github上获取脚本：

    bash <(curl -L "https://raw.githubusercontent.com/FirstJavaMaster/easy-script/master/backup-mysql/install.sh")

脚本会自动在当前目录创建 `backup_mysql` 文件夹，并下载最新的脚本代码到目录里

脚本访问数据库需要用户配置 `login-path`。如何配置请参考：https://www.jianshu.com/p/feb178a677a2

脚本会将备份的文件放在 `/data/backups/mysql/{数据库名}` 目录下。
