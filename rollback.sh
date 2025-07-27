#!/bin/bash
set -eo pipefail

# 日志设置
LOG_FILE="rollback_$(date +%Y%m%d%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=== 开始回滚 $(date) ==="

# 回滚数据库
rollback_migrations() {
  echo "回滚数据库变更..."
  last_migration=$(python manage.py showmigrations | grep '[X]' | tail -1 | awk '{print $2}')
  if [ -n "$last_migration" ]; then
    python manage.py migrate $last_migration
  fi
}

# 清理构建产物
clean_artifacts() {
  echo "清理构建文件..."
  rm -rf staticfiles/ __pycache__/ *.pyc
}

# 主回滚流程
main() {
  rollback_migrations
  clean_artifacts
  
  echo "=== 回滚成功完成 ==="
  exit 0
}

main