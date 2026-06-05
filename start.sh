#!/bin/bash
# 聚宁数据门户 - 本地一键启动脚本
# 用法: bash start.sh

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "================================"
echo "  聚宁数据 - 本地启动"
echo "================================"

# 1. 安装后端依赖
echo ""
echo "[1/4] 检查后端依赖..."
pip install -q fastapi uvicorn sqlalchemy pymysql cryptography pydantic python-multipart 2>/dev/null

# 2. 安装前端依赖
echo "[2/4] 检查前端依赖..."
cd "$PROJECT_DIR/frontend"
pnpm install --frozen-lockfile 2>/dev/null || pnpm install

# 3. 启动后端 (端口 8000)
echo "[3/4] 启动后端 API (端口 8000)..."
cd "$PROJECT_DIR"
python -u server/main.py &
BACKEND_PID=$!
echo "  后端 PID: $BACKEND_PID"

# 等待后端就绪
sleep 2

# 4. 启动前端 (端口 5000)
echo "[4/4] 启动前端 (端口 5000)..."
cd "$PROJECT_DIR/frontend"
pnpm dev &
FRONTEND_PID=$!
echo "  前端 PID: $FRONTEND_PID"

echo ""
echo "================================"
echo "  启动完成!"
echo "  前端: http://localhost:5000"
echo "  后端: http://localhost:8000"
echo "  API 文档: http://localhost:8000/docs"
echo "================================"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获退出信号，杀掉子进程
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

# 等待
wait
