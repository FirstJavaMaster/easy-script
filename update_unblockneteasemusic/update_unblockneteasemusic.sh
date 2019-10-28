#!/bin/bash

source /etc/profile

# 打印时间
echo ""
time=$(date '+%Y-%m-%d %H:%M:%S')
echo "开始执行脚本 ${time}"

# 更新docker镜像
docker pull nondanee/unblockneteasemusic

# 重启容器
docker-compose -f /data/docker-compose/unblock-netease-music.yml up -d

# 清理陈旧镜像
docker system prune --force

