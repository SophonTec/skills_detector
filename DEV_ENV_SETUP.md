# 开发环境配置记录

## 本地开发环境

### 系统信息
- **操作系统**: macOS (Darwin)
- **CPU 架构**: arm64 (Apple Silicon)
- **Python 版本**: 3.13.11 (推荐使用，3.14.2 有兼容性问题)
- **Node.js 版本**: v25.4.0
- **Docker 版本**: 29.1.2

---

## Python 环境配置

### 推荐配置

```bash
# 使用 Python 3.13（不是 3.14，因为有包兼容性问题）
/opt/homebrew/opt/python@3.13/bin/python3.13 -m venv venv
source venv/bin/activate

# 安装基础包
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic pydantic-settings httpx python-dotenv apscheduler
```

### 避免的包

```python
# ❌ 不建议安装（需要编译，Python 3.14 有问题）
playwright==1.40.0  # 需要 Rust 编译，兼容性差
greenlet             # Python 3.14 兼容性问题
pydantic-core        # Python 3.14 兼容性问题

# ✅ 建议使用最新稳定版
pip install fastapi uvicorn sqlalchemy
```

### 后端启动命令

```bash
# 开发模式（带热重载）
export DATABASE_ENCRYPTION_KEY=your-key-here
export SECRET_KEY=your-secret-here
export DATABASE_PATH=/tmp/skills.db
export FRONTEND_URL=http://localhost:3000

source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

---

## Node.js 环境配置

### 安装依赖

```bash
cd frontend
npm install --silent
```

### 环境变量

```bash
# Next.js 需要 API URL
export NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 前端启动命令

```bash
# 开发模式
npm run dev

# 生产构建
npm run build
npm start
```

---

## Docker 环境（问题记录）

### Docker Hub 访问问题

**问题**: TLS handshake timeout
**原因**: 网络环境限制（Docker Hub 超时）
**临时方案**: 本地直接运行服务

### 建议的 Docker 配置（国内）

```yaml
# daemon.json 配置
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.nju.edu.cn",
    "https://dockerproxy.com"
  ]
}
```

---

## Git 配置

### 初始化和提交

```bash
# 初始化仓库
git init
git branch -M main

# 添加所有文件
git add .

# 提交（遵循约定式提交）
git commit -m "feat: initial commit - AI Skills Tracker

- Backend: FastAPI with multi-source scrapers
- Frontend: Next.js with sorting and filtering
- Deployment: Docker Compose setup
- Documentation: Complete README, deployment guide, and design docs"
```

### 远程仓库配置

```bash
# HTTPS 需要凭证
git remote add origin https://github.com/username/repo.git

# SSH 推荐（免密钥，更方便）
git remote add origin git@github.com:username/repo.git

# 推送
git push -u origin main
```

### 忽略文件配置

```gitignore
# 环境文件
.env
.env.local
.env.*.local

# 数据库
*.db
*.db-shm
*.db-wal
data/

# Python
__pycache__/
*.pyc
venv/
env/

# Node
node_modules/
.next/
out/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db
```

---

## 数据库配置

### SQLite 开发设置

```python
# 数据库路径
DATABASE_PATH = "/tmp/skills.db"

# 连接配置
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# 加密配置（SQLCipher - 可选）
# DATABASE_ENCRYPTION_KEY = "your-32-character-key"
```

### 数据库迁移

```bash
# 删除旧数据库
rm /tmp/skills.db

# 重新启动服务器
uvicorn app.main:app --reload
# 自动创建新数据库
```

---

## API 测试配置

### 测试脚本

```bash
#!/bin/bash
# scripts/test.sh

API_URL="${API_URL:-http://localhost:8000}"

# 健康检查
curl -s "${API_URL}/api/v1/health" | jq .

# 统计信息
curl -s "${API_URL}/api/v1/stats" | jq .

# 技能列表
curl -s "${API_URL}/api/v1/skills?sort=latest&limit=5" | jq .
```

### 测试端点

| 端点 | 方法 | 测试数据 |
|------|------|---------|
| `/api/v1/health` | GET | 状态检查 |
| `/api/v1/stats` | GET | 统计数据 |
| `/api/v1/skills` | GET | 技能列表 + 排序/过滤 |
| `/api/v1/skills/{id}` | GET | 单个技能 |
| `/api/v1/scrapes` | GET | 爬虫日志 |
| `POST /api/v1/scrape/{source}` | POST | 手动触发爬虫 |

---

## 调试配置

### 后端调试

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# FastAPI 调试
# uvicorn app.main:app --reload --port 8000 --log-level debug
```

### 前端调试

```bash
# 开发模式自动启用热重载和错误堆栈
npm run dev

# 浏览器开发工具
# - React DevTools
# - Network 标签（查看 API 请求）
# - Console 标签（查看错误）
```

### 数据库调试

```python
# 查看数据库内容
import sqlite3
conn = sqlite3.connect('skills.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM skills LIMIT 10")
print(cursor.fetchall())
```

---

## 性能优化

### 后端优化

```python
# 使用连接池
from sqlalchemy.pool import QueuePool
engine = create_engine(DATABASE_URL, poolclass=QueuePool, pool_size=10)

# 启用 SQLAlchemy 查询缓存
from sqlalchemy.orm import scoped_session
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
```

### 前端优化

```typescript
// React.memo 避免不必要的重新渲染
const SkillCard = React.memo(({ skill }) => {
  return <div>...</div>
});

// 使用 useMemo 缓存计算结果
const sortedSkills = useMemo(() => {
  return skills.sort((a, b) => b.stars - a.stars);
}, [skills]);
```

---

## 常用命令速查

### Python

```bash
# 激活虚拟环境
source venv/bin/activate

# 退出虚拟环境
deactivate

# 安装单个包
pip install package-name

# 查看已安装包
pip list

# 导出依赖
pip freeze > requirements.txt

# 从 requirements 安装
pip install -r requirements.txt
```

### Node.js

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build

# 预览生产构建
npm run preview

# 清理
npm run clean

# 检查过时依赖
npm outdated
```

### Git

```bash
# 查看状态
git status

# 查看改动
git diff

# 查看提交历史
git log --oneline

# 撤销工作区改动
git checkout -- .

# 撤销暂存区
git restore --staged .

# 创建分支
git branch feature-name

# 切换分支
git checkout feature-name

# 合并分支
git merge feature-name

# 删除分支
git branch -d feature-name
```

### Docker

```bash
# 构建镜像
docker compose build

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看容器状态
docker compose ps

# 进入容器
docker compose exec backend bash
```

---

## 环境检查脚本

```bash
#!/bin/bash
# scripts/check_env.sh

echo "检查开发环境..."

# Python 检查
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python: $PYTHON_VERSION"
else
    echo "❌ Python 未安装"
fi

# Node.js 检查
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Node.js 未安装"
fi

# npm 检查
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm: $NPM_VERSION"
else
    echo "❌ npm 未安装"
fi

# Docker 检查
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "✅ Docker: $DOCKER_VERSION"
else
    echo "❌ Docker 未安装"
fi

# Docker Compose 检查
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    echo "✅ Docker Compose: $COMPOSE_VERSION"
else
    echo "⚠️  Docker Compose 未安装（使用 docker compose）"
fi

# Git 检查
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✅ Git: $GIT_VERSION"
else
    echo "❌ Git 未安装"
fi

echo ""
echo "环境检查完成！"
```

---

## IDE 配置

### VS Code 推荐扩展

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-vscode-remote.remote-containers",
    "eamodio.gitlens"
  ]
}
```

### VS Code 工作区配置

```json
{
  "folders": [
    {
      "path": "./backend",
      "name": "Backend (FastAPI)"
    },
    {
      "path": "./frontend",
      "name": "Frontend (Next.js)"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
  }
}
```

---

## 故障排除

### Python 问题

**问题**: 模块导入错误
```bash
# 解决方案 1: 检查虚拟环境是否激活
which python

# 解决方案 2: 重新安装依赖
pip install --force-reinstall package-name

# 解决方案 3: 清理 Python 缓存
pip cache purge
```

### Node.js 问题

**问题**: 模块找不到
```bash
# 解决方案: 清理并重新安装
rm -rf node_modules package-lock.json
npm install
```

### Docker 问题

**问题**: 容器无法启动
```bash
# 查看详细日志
docker compose logs backend

# 检查端口占用
lsof -i :8000

# 清理并重启
docker compose down -v
docker compose up -d --build
```

---

## 下次启动项目

### 快速启动命令

```bash
# 终端 1: 后端
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# 终端 2: 前端
cd frontend
npm run dev
```

### 使用 Docker 启动

```bash
# 配置环境
cp .env.example .env
nano .env

# 启动
docker compose up -d

# 查看日志
docker compose logs -f
```

---

*最后更新: 2026-02-03*
*适用于: macOS/Linux/Windows 开发环境*
