#!/bin/bash

# 更新docker镜像
docker pull nondanee/unblockneteasemusic

# 重启容器
docker-compose -f /data/docker-compose/unblock-netease-music.yml up -d

# 清理陈旧镜像
docker system prune --force
