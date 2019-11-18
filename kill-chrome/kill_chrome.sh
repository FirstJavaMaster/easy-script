kill -9 "$(ps -ef | grep chrome | grep -v grep | awk '{print $2}')"
