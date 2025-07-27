#!/bin/bash
set -eo pipefail

# 初始化日志
LOG_FILE="deploy_$(date +%Y%m%d%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== 开始部署 $(date) ==="

# 环境检查
check_environment() {
  echo "验证部署环境..."
  [ -f ".env" ] || { echo "缺少.env配置文件"; exit 1; }
  python --version || { echo "Python不可用"; exit 1; }
}

# 安装依赖
install_dependencies() {
  echo "安装依赖..."
  pip install -r requirements.txt --no-cache-dir
}

# 数据库迁移
run_migrations() {
  echo "执行数据库迁移..."
  python manage.py migrate --no-input
}

# 静态文件收集
collect_static() {
  echo "收集静态文件..."
  python manage.py collectstatic --no-input
}

# 主部署流程
main() {
  check_environment
  install_dependencies
  run_migrations
  collect_static
  
  echo "=== 部署成功完成 ==="
  exit 0
}

main