#!/bin/bash -e

# $1:数据库名, $2:文件存放路径
database=$1
target_dir=$2

time=$(date +%Y%m%d_%H%M)
file_name="${database}_mysql_backup_${time}"

tmp_file=${file_name}.sql
tar_file=${target_dir}/${file_name}.tar.gz

echo ""
echo "开始备份数据库: ${database}"
echo "导出sql文件: ${tmp_file}"
cd /tmp
mysqldump --login-path=slkj --databases "${database}" > "${tmp_file}"

echo "压缩到文件: ${tar_file}"
tar -czPf "${tar_file}" "${tmp_file}"

echo "清理临时sql文件..."
rm -f "${tmp_file}"

echo ""
echo "删除过期备份..."
find "${target_dir}" -mtime +30 -type f -name "*.tar.gz" -print -exec rm -rf {} \;

echo "备份完成"
