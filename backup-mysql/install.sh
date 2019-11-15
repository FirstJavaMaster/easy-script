#!/bin/bash

shell_dir_name="backup_mysql"

echo "检查目录 ${shell_dir_name} 是否存在"
if [ ! -d ${shell_dir_name} ]; then
  echo "创建目录"
  mkdir "${shell_dir_name}"
fi

cd ${shell_dir_name} || exit

echo "下载脚本..."
wget "https://raw.githubusercontent.com/FirstJavaMaster/easy-script/master/backup-mysql/main.sh" -O "main.sh"
wget "https://raw.githubusercontent.com/FirstJavaMaster/easy-script/master/backup-mysql/worker.sh" -O "worker.sh"

chmod 755 -R ./*.sh

echo "安装完毕"
echo ""