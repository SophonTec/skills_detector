#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         AI Skills Tracker - Ubuntu 24.04 部署脚本               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

echo "📋 第1步：系统更新..."
apt update && apt upgrade -y

echo ""
echo "🐳 第2步：安装 Docker..."
apt install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo ""
echo "👤 第3步：添加当前用户到 docker 组..."
USERNAME=${SUDO_USER:-$(whoami}
usermod -aG docker $USERNAME

echo ""
echo "🔥 第4步：启动 Docker..."
systemctl enable docker
systemctl start docker

echo ""
echo "✅ Docker 安装完成！"
echo ""
echo "⚠️  重要：注销并重新登录以应用 docker 组权限"
echo "   或者运行: newgrp docker"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
