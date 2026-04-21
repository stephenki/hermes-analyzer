#!/bin/bash
cd ~/projects/hermes-analyzer
echo "📦 项目目录: $(pwd)"
git status
echo ""
echo "请选择操作方式:"
echo "1. 自动创建（需 gh CLI）: gh repo create hermes-analyzer --public --source=. --remote=origin"
echo "2. 手动创建: 访问 https://github.com/new 创建空仓库后运行:"
echo "   git remote add origin git@github.com:stephenki/hermes-analyzer.git"
echo "   git push -u origin main"
