#!/bin/bash
#############################################
## 作者：京城郭少
## 作用：启停脚本
## 最后一次修改时间：2022-11-12
#############################################
app=listenKey.py

# 启动app
function app_start(){
    # check服务是否存活,如果存在则返回
    get_status
    local running=$?
    if [ ${running} -ne 0 ]; then
        local pid=$(get_pid)
        echo "${app} is already started, pid=${pid}"
        return 0
    fi

    #启动程序
    nohup python3 ./${app} &
    sleep 1

    # 检查服务是否启动成功
    get_status
    local running=$?
    if [ ${running} -eq 0 ];then
        echo "${app} start failed, please check"
        return 1
    fi

    local pid=$(get_pid)
    echo "${app} start ok, pid=${pid}"
    return 0
}
# 停止app
function app_stop() {
    # check服务是否存活,如果已停止则直接返回
    get_status
    local running=$?
    if [ ${running} -ne 1 ]; then
        echo "${app} is already stoped"
        return 0
    fi


    # 循环stop服务, 直至60s超时
    pid=$(get_pid)
    echo "app will be stoped,pid=$pid"
    for (( i = 0; i < 30; i++ )); do
        # 停止该服务
        kill -15 ${pid}

        #等待进程退出
        sleep 2

        # 检查服务是否停止,如果停止则直接返回
        get_status
        if [ $? -eq 0 ];then
           echo "${app} is stopped"
           return 0
        fi
    done

    # stop服务失败, 返回码为 非0
    echo "stop timeout(60s)"
    return 1
}

# 查看进程状态
function app_status(){
    get_status
    local running=$?

    if [ ${running} -eq 0 ]; then
        echo "${app} is stopped!"
        return 0
    fi

    #local status_http_code=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/v1/health)
    #if [ ${status_http_code} -ne 200 ]; then
    #    echo "${app} is broken down, status interface got http code ${status_http_code}"
    #    return 1
    #fi

    local pid=$(get_pid)
    echo "${app} is started, pid=${pid}"
    return 1
}

# 获取进程状态
# return 0 表示进程未启动
# return 1 表示进程启动
function get_status(){
    pid=$(get_pid)
    if [ "x_" != "x_${pid}" ]; then
        running=$(ps -p ${pid}|grep -v "PID TTY" |wc -l)
        return ${running}
    fi
    return 0
}

#获取app的pid
function get_pid() {
    /bin/ps aux | grep $app | grep -v grep | awk '{print $2}'
}

action=$1
case $action in
    "start" )
        # 启动服务
        app_start
        ;;
    "stop" )
        # 停止服务
        app_stop
        ;;
    "status" )
        # 检查服务
        app_status false
        ;;
    "restart" )
        # 重启服务
        app_stop
        sleep 2
        app_start
        ;;
    "debug" )
        #debug
        app_stop
        ;;
    * )
        echo "unknown command"
        exit 1
        ;;
esac
