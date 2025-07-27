#!/bin/zsh
# 安全巡检脚本
CONFIG_DIR="/Users/iohongiong/comate-zulu-demo-1753124168900/meme_tracker/config"
LOG_FILE="$CONFIG_DIR/SECURITY.log"

echo "=== $(date +'%Y-%m-%d') 安全检查 ===" >> $LOG_FILE
stat -f "%Sp %N" $CONFIG_DIR/.env* 2>/dev/null >> $LOG_FILE
find $CONFIG_DIR -name ".*env*" -exec ls -la {} \; >> $LOG_FILE
