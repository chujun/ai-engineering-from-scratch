#!/bin/bash
# Jupyter Lab 服务启动脚本
# 用法: ./start-jupyter-lab-service.sh [start|stop|restart|status]

NAME="jupyter-lab"
PORT=8888
IP=0.0.0.0
LOG_DIR="/tmp/jupyter-logs"
LOG_FILE="${LOG_DIR}/${NAME}.log"
PID_FILE="/tmp/${NAME}.pid"

mkdir -p "${LOG_DIR}"

get_pid() {
    if [ -f "${PID_FILE}" ]; then
        cat "${PID_FILE}"
    fi
}

is_running() {
    local pid=$(get_pid)
    if [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null; then
        return 0
    fi
    return 1
}

start() {
    if is_running; then
        echo "${NAME} 已在运行 (PID: $(get_pid))"
        return 0
    fi

    echo "启动 ${NAME}..."
    nohup jupyter lab --no-browser --port=${PORT} --ip=${IP} --allow-root > "${LOG_FILE}" 2>&1 &
    local pid=$!
    echo "${pid}" > "${PID_FILE}"
    sleep 2

    if is_running; then
        echo "${NAME} 启动成功 (PID: ${pid})"
        echo "日志: ${LOG_FILE}"
        echo "访问: http://localhost:${PORT}"
    else
        echo "${NAME} 启动失败，查看日志: ${LOG_FILE}"
        return 1
    fi
}

stop() {
    if ! is_running; then
        echo "${NAME} 未运行"
        rm -f "${PID_FILE}"
        return 0
    fi

    echo "停止 ${NAME} (PID: $(get_pid))..."
    kill $(get_pid) 2>/dev/null
    rm -f "${PID_FILE}"
    echo "${NAME} 已停止"
}

status() {
    if is_running; then
        echo "${NAME} 正在运行 (PID: $(get_pid))"
        echo "日志: ${LOG_FILE}"
    else
        echo "${NAME} 未运行"
    fi
}

case "${1}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    status)
        status
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
