# 将本地文件上传到对应的服务器上去, 简化键盘敲击次数, 不必记忆访问host和username

action=$1
file=$2

user=root
host=8.8.8.8

do_ssh(){
  ssh ${user}@${host}
}

do_scp(){
  if [ -z "${file}" ]
  then
    echo "请输入要传输的文件"
    exit 1
  elif [ ! -e "${file}" ]
  then
    echo "文件不存在"
    exit 2
  fi

  scp -r "${file}" ${user}@${host}:~
}

case ${action} in
ssh)
  do_ssh
  ;;
scp)
  do_scp
  ;;
*)
  if [ -z "${action}" ]; then
    do_ssh
  else
    echo "请输入 ssh 或 scp 命令 以执行相应的功能"
  fi
  ;;
esac
