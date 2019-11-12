# 将本地文件上传到对应的服务器上去, 简化键盘敲击次数, 不必记忆访问host和username
# 支持多文件上传

# 命令
action=$1

# 要传递的文件
params=$*
files=${params#scp}

user=root
host=8.8.8.8

do_ssh(){
  ssh ${user}@${host}
}

do_scp(){
  if [ -z "${files}" ]
  then
    echo "请输入要传输的文件"
    exit 1
  elif [ ! -e "${files}" ]
  then
    echo "文件不存在"
    exit 2
  fi

  scp -r "${files}" ${user}@${host}:~
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
