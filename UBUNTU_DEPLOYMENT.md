# Ubuntu 24.04 部署指南

## 硬件资源评估

| 资源 | 需求 | 你的配置 | 评估 |
|------|------|----------|------|
| CPU | 2 cores | AMD 3955WX (64+ cores) | ✅ 远超需求 |
| 内存 | 2GB | 256GB | ✅ 远超需求（可用作缓存）|
| 显存 | 不需要 | 96GB | ✅ 不需要但可用 |
| 磁盘 | 10GB | - | ⏳ 建议SSD 50GB+ |

**结论**：你的服务器配置**完全满足且远超**项目需求，还可以运行其他服务。

---

## 部署方案选择

### 方案 1：Docker 部署（推荐生产环境）

**优点**：
- 环境隔离，易于管理
- 版本一致性
- 快速部署和回滚
- 适合生产环境

**缺点**：
- 需要 Docker 安装

---

### 方案 2：本地直接运行

**优点**：
- 无需 Docker
- 直接访问系统资源

**缺点**：
- 依赖管理复杂
- 不适合生产环境

---

## 推荐部署流程（Docker 方式）

### 第1步：安装 Docker

```bash
# 使用提供的安装脚本
cd /path/to/skill_detector
sudo bash deploy/ubuntu_install_docker.sh

# 或手动安装
sudo apt update
sudo apt install -y docker.io docker-compose-plugin

# 启动 Docker
sudo systemctl enable docker
sudo systemctl start docker

# 添加当前用户到 docker 组
sudo usermod -aG docker $USER
newgrp docker
```

### 第2步：克隆项目

```bash
git clone git@github.com:SophonTec/skills_detector.git
cd skills_detector
```

### 第3步：配置环境变量

```bash
# 复制环境模板
cp .env.example .env

# 编辑配置
nano .env
```

**必须配置**：
```bash
# 生成安全密钥
DATABASE_ENCRYPTION_KEY=<32字符密钥>
SECRET_KEY=<32字符密钥>
```

**可选配置**：
```bash
# GitHub Token（提高速率限制）
# 生成: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

### 第4步：启动服务

```bash
# 构建并启动
docker compose up -d

# 查看日志
docker compose logs -f

# 查看服务状态
docker compose ps
```

### 第5步：验证部署

```bash
# 健康检查
curl http://localhost/api/v1/health

# 统计信息
curl http://localhost/api/v1/stats
```

### 第6步：配置 HTTPS（生产环境推荐）

使用 Let's Encrypt 免费 SSL 证书：

```bash
# 安装 certbot
sudo apt install -y certbot

# 生成证书（需要域名）
sudo certbot certonly --standalone -d yourdomain.com

# 更新 nginx 配置使用 SSL
# 编辑 nginx/nginx.conf
# 取消 SSL 相关配置的注释

# 重启 nginx
docker compose restart nginx
```

---

## 端口配置

| 服务 | 内部端口 | 外部端口 | 说明 |
|------|----------|----------|------|
| Nginx | 80, 443 | 80, 443 | Web访问 |
| Backend | 8000 | - | 内部通信 |
| Frontend | 3000 | - | 内部通信 |

**防火墙配置**：
```bash
# 允许 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
```

---

## 性能优化建议

### 利用你的强大硬件

虽然项目不需要强大硬件，但可以优化其他方面：

#### 1. 数据库缓存

你的 256GB 内存可用作缓存：

```bash
# 配置 Redis（可选）
docker compose -f docker-compose.redis.yml up -d
```

#### 2. 增加爬虫并发

利用 CPU 多核：

```bash
# 编辑 backend/app/services/scheduler.py
# 增加并发爬虫数量
```

#### 3. 配置系统服务

```bash
# 安装 systemd 服务
sudo cp ai-skills-tracker.service /etc/systemd/system/
sudo systemctl enable ai-skills-tracker
sudo systemctl start ai-skills-tracker
```

#### 4. 配置监控

利用你的 GPU 做其他用途：

```bash
# 可以部署 Grafana + Prometheus 监控
# 可以运行其他 AI 服务
```

---

## 生产环境检查清单

- [ ] 安装 Docker 和 Docker Compose
- [ ] 克隆项目代码
- [ ] 配置环境变量（.env）
- [ ] 配置 GitHub Token（可选但推荐）
- [ ] 启动 Docker 服务
- [ ] 验证 API 健康状态
- [ ] 配置 HTTPS（生产环境）
- [ ] 配置防火墙规则
- [ ] 设置 systemd 自动启动
- [ ] 配置数据库备份计划
- [ ] 配置日志轮转
- [ ] 设置监控告警

---

## 常见问题

### Q1: 是否需要 AI 模型？
**A**: 不需要。这个项目只抓取和展示元数据，不需要运行任何 AI 模型。

### Q2: GPU 如何使用？
**A**: 项目不需要 GPU。你的 RTX Pro 6000 可以用于：
- 运行其他 AI 服务
- 部署独立的推理服务
- 用于开发测试

### Q3: 需要公网 IP 吗？
**A**: 是的，需要访问外部 API（GitHub/npm/PyPI/HuggingFace）。如果是内网，需要配置代理。

### Q4: 需要域名吗？
**A**: 不是必需的，可以用 IP 访问。但配置 HTTPS 需要域名。

### Q5: 如何备份数据库？
**A**:
```bash
# 每日自动备份
crontab -e
# 添加: 0 2 * * * /path/to/skill_detector/scripts/backup.sh
```

---

## 监控和维护

### 查看服务状态

```bash
# Docker 服务
docker compose ps

# 系统服务
sudo systemctl status ai-skills-tracker

# API 健康检查
watch -n 5 'curl -s http://localhost/api/v1/health | jq'
```

### 日志管理

```bash
# 实时日志
docker compose logs -f

# 日志文件
tail -f /var/log/ai-skills-tracker/*.log
```

### 数据库维护

```bash
# 查看数据库大小
du -sh /path/to/data/skills.db

# 清理旧数据（可选）
# 保留最近 90 天的 metrics
```

---

## 扩展建议

### 利用你的服务器能力

1. **部署其他服务**：
   - Grafana/Prometheus 监控
   - Jupyter Notebook 用于数据分析
   - 独立的 AI 推理服务

2. **数据可视化**：
   - 部署 Grafana Dashboard
   - 实时展示技能趋势

3. **高级功能**：
   - 添加用户认证
   - 技能推荐系统
   - 趋势预测（可用你的 GPU）

---

## 快速部署命令汇总

```bash
# 1. 安装 Docker
sudo bash deploy/ubuntu_install_docker.sh

# 2. 克隆项目
git clone git@github.com:SophonTec/skills_detector.git
cd skills_detector

# 3. 配置环境
cp .env.example .env
nano .env

# 4. 启动服务
docker compose up -d

# 5. 验证
curl http://localhost/api/v1/health

# 6. 配置系统服务（可选）
sudo systemctl enable ai-skills-tracker
sudo systemctl start ai-skills-tracker
```

---

**部署时间估计**: 15-30 分钟（取决于网络速度）

**维护需求**: 低 - 自动化运行，仅需定期检查

---

*最后更新: 2026-02-03*
*适用版本: Ubuntu 24.04 LTS*
