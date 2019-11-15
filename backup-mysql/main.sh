#!/bin/bash

#不备份的数据库,以"|"进行分割
exclude_databases="Database|information_schema|performance_schema|mysql|sys|opsmanage"

#备份文件存储路径
backup_dir=/data/backups/mysql

# 当前时间
time=`date +%Y%m%d_%H%M`
# 备份过程中是否出现异常
exist_error=false
#错误信息发送的邮件
error_email=tongpc@idx365.com

#脚本所在路径
workspace=`cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd`
#日志文件所在地址,用于出现错误时发送邮件
log_file=${workspace}/mysql_backup.log


#开始备份之前，将备份信息头写入日记文件
echo "======================================"
echo "备份脚本启动 ${time} :"

#判断备份文件存储目录是否存在，否则创建该目录
if [[ ! -d ${backup_dir} ]]
then
    mkdir -p ${backup_dir}
fi

# "获取mysql里所有的数据库"
databases=`mysql --login-path=slkj -e "SHOW DATABASES;" | tr -d "| " | grep -Ev ${exclude_databases}`

for db in ${databases}
do
    database_backup_dir=${backup_dir}/${db}
    if [[ ! -d ${database_backup_dir} ]] ; then
        mkdir -p ${database_backup_dir}
    fi

    sh -e ${workspace}/worker.sh ${db} ${database_backup_dir}

    if [[ $? -ne 0 ]]; then
        echo "${db} 备份失败!!!"
        exist_error=true
    fi
done

if ${exist_error}; then
    ip=`ip addr | grep 'state UP' -A2 | sed -n '3p' | awk '{print $2}' | awk -F"/" '{print $1}'`
    mail -s "数据库备份异常 - ${ip}" ${error_email} < tail -n 50 ${log_file}
fi

echo ""
echo "删除空文件夹"
find ${backup_dir} -type d -empty -print -exec rm -rf {} \;

echo "备份脚本结束"
echo ""
