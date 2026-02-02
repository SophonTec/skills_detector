# 开发经验总结 - AI Skills Tracker

## 项目概述

**开发时间**: 2026-02-03
**开发模式**: Plan-Driven Development (计划驱动开发)
**最终状态**: ✅ 完全交付并测试通过

---

## 开发流程总结

### Phase 0: 意图门控

**关键经验**: 每次接收用户请求时，先分类请求类型

| 类型 | 信号 | 行动 |
|------|------|------|
| 显性请求 | 具体文件/命令 | 直接执行工具 |
| 探索性 | "如何X工作"、"找Y" | 触发 explore 代理 |
| 开放性 | "改进"、"重构"、"添加功能" | 先评估代码库 |
| 模糊性 | 不清楚范围/多种解释 | 必须问一个问题 |

**经验教训**：
1. ✅ **立即分类** - 不要盲目行动
2. ✅ **检查模糊性** - 多种解释 >2x 差异 → 必须问
3. ✅ **委托优于自己** - 除非超级简单

---

### Phase 1: 代码库评估

**关键经验**: 先评估代码库是否成熟，决定遵循风格还是提出改进

| 状态 | 信号 | 行为 |
|------|------|------|
| 纪律性 | 一致模式、配置文件 | 严格遵循风格 |
| 过渡性 | 混合模式、部分结构 | 询问用户偏好 |
| 遗留/混乱 | 无一致性、过时模式 | 提出现代化方案 |
| 绿地 | 新/空项目 | 应用现代最佳实践 |

**经验教训**：
1. ✅ **检查配置文件** - linter, formatter, type config
2. ✅ **采样相似文件** - 找到真实模式，不要假设
3. ✅ **注意项目年龄信号** - 依赖、模式

---

### Phase 2: 探索与研究

**关键经验**: 正确使用探索和引用代理

| 需求类型 | 工具 | 用途 |
|------------|------|------|
| 内部代码搜索 | `explore` | 在代码库中找到模式 |
| 外部文档/开源 | `librarian` | GitHub CLI, Context7, Web Search |
| 复杂架构设计 | `oracle` | 只读、高智能推理 |
| 计划前分析 | `metis` | 识别隐藏意图、模糊性 |
| 工作计划审查 | `momus` | 评估清晰性、可验证性、完整性 |

**经验教训**：
1. ✅ **并行执行探索** - 同时启动多个 `explore` 和 `librarian`
2. ✅ **探索是 Grep 不是顾问** - 快速、后台、轻量
3. ✅ **用完再收集** - 后台运行，需要时用 `background_output(task_id=...)`
4. ✅ **停止搜索条件** - 足够上下文、重复信息、2次迭代无新数据
5. ✅ **不要过度探索** - 时间宝贵，只收集必要信息

**错误案例**：
- ❌ 顺序调用探索代理（太慢）
- ❌ 等待探索完成再工作（应该并行）
- ❌ 搜索超过需要（浪费时间）

---

### Phase 3: 实现策略

**关键经验**: 委托是默认，自己工作仅当超级简单

### 委托模式

```python
# 委托任务的基本模式
delegate_task(
    category="[selected-category]",  # 必须选择最合适的类别
    load_skills=["skill-1", "skill-2"],  # 必须包含所有相关技能
    prompt="...",
    run_in_background=False  # 通常同步等待结果
)
)
```

### 类别选择

| 类别 | 最佳使用场景 | 描述 |
|------|------------|------|
| `visual-engineering` | 前端、UI/UX、设计、动画 | 前端工作委托给此 |
| `ultrabrain` | 真正困难、逻辑繁重的任务 | 只用于硬问题，不是简单实现 |
| `deep` | 目标驱动的自主问题解决 | 需要深入理解的复杂问题 |
| `artistry` | 非常规、创造性的解决方案 | 超越标准模式 |
| `quick` | 微不足道的任务 | 单文件更改、拼写错误修复 |
| `unspecified-low` | 不适合其他类别、低工作量 | 不明确的任务，低努力 |
| `unspecified-high` | 不适合其他类别、高工作量 | 不明确的任务，高努力 |
| `writing` | 文档、散文、技术写作 | 文档、技术写作 |

### 技能选择

必须评估每个技能：

| 技能 | 领域 | 何时包含 |
|------|------|----------|
| `playwright` | 浏览器自动化 | 任何浏览器相关任务（MUST USE）|
| `frontend-ui-ux` | UI/UX 设计 | 设计师出身的开发人员 |
| `git-master` | Git 操作 | 任何 git 操作（MUST USE）|
| `dev-browser` | 浏览器自动化 | 持久页面状态的浏览器自动化 |

**经验教训**：
1. ✅ **先读技能描述** - 确保领域匹配
2. ✅ **必须证明省略** - 如果不包含可能相关的技能，解释为什么
3. ✅ **不要省略所有技能** - 空 `load_skills=[]` 是被禁止的反模式

**反模式示例**：
```python
# ❌ 错误：省略所有技能
delegate_task(category="quick", load_skills=[], prompt="...")

# ✅ 正确：包含所有相关技能
delegate_task(category="visual-engineering", 
            load_skills=["frontend-ui-ux"], 
            prompt="...")
```

---

### Phase 4: 任务管理

**关键经验**: 为非平凡任务创建 TODO 列表

### 何时创建 TODO

| 触发 | 行动 |
|------|------|
| 多步骤任务（2+步骤）| 总是立即创建 |
| 不确定范围 | 总是（TODO 澄清思维）|
| 用户请求多个项目 | 总是 |
| 复杂单任务 | 创建 TODO 来分解 |

### TODO 最佳实践

```python
# 立即创建 - 不要宣布
todowrite(todos=[
    {"id": "task-1", "content": "...", "status": "in_progress", "priority": "high"},
    # ... 更多任务
])

# 在开始前标记 in_progress
# 在完成后立即标记 completed（不要批处理）
# 只有一个任务处于 in_progress
```

**经验教训**：
1. ✅ **立即创建** - 接收请求后立即
2. ✅ **超级详细** - 原子步骤，易于追踪
3. ✅ **实时更新** - 立即标记完成
4. ✅ **不要批处理** - 每个任务完成后更新
5. ✅ **如果范围改变，先更新 TODO** - 不要盲目继续

---

### Phase 5: 代码变更

**关键经验**: 遵循约束，不要投机

### 硬约束（不能违反）

| 约束 | 不可做 |
|------|--------|
| 类型错误抑制 | `as any`, `@ts-ignore`, `@ts-expect-error` |
| 未显式请求提交 | 永远不提交 |
| 投机未读代码 | 永远不假设读 |
| 留下代码破坏状态 | 失败后永不让状态 |
| 删除失败测试以"通过" | 禁止 |
| 散弹调试 | 随机更改希望有效 | 禁止 |

### 软约束（最佳实践）

| 约束 | 建议 |
|------|------|
| 优先现有库 | 而非新依赖 |
| 优先小聚焦更改 | 而非大型重构 |
| 不确定时问 | 不要猜测 |
| 用户设计有问题时 | 提出，不要盲目实现 |

### Bug 修复规则

**最小修复原则**：
```python
# ✅ 正确：只修复 bug
if bug_condition:
    fix_bug()

# ❌ 错误：在修复期间重构
if bug_condition:
    refactor_related_code()
    add_new_feature()
    fix_bug()
```

---

### Phase 6: 验证

**关键经验**: 任务不完成直到提供证据

### 证据要求

| 行动 | 必需证据 |
|------|----------|
| 文件编辑 | `lsp_diagnostics` 在更改文件上干净 |
| 构建命令 | 退出码 0 |
| 测试运行 | 通过（或明确说明预先存在的失败）|
| 委托 | 代理结果已接收并验证 |

**无证据 = 不完整**

---

### Phase 7: 故障恢复

**关键经验**: 系统化的失败处理

### 失败后 3 次停止

1. **停止所有编辑** - 立即停止
2. **恢复到最后的已知良好状态** - `git checkout / undo edits`
3. **记录尝试内容和失败** - 什么被尝试，什么失败了
4. **咨询 Oracle** - 带完整失败上下文
5. **如果 Oracle 不能解决 → 问用户** - 在继续前

**永不要**：
- ❌ 留下代码破坏状态
- ❌ 继续希望它将工作
- ❌ 删除失败测试以"通过"

---

### Phase 8: 完成

**关键经验**: 完成前检查

### 任务完成检查表

- [ ] 所有计划 TODO 项目标记为完成
- [ ] 更改文件上的 `lsp_diagnostics` 干净
- [ ] 构建通过（如适用）
- [ ] 测试通过（如适用）
- [ ] 用户原始请求完全解决

### 完成前

**永不要省略**：
- 取消所有运行中的后台任务: `background_cancel(all=true)`
- 这节省资源并确保干净工作流

---

## 环境配置记录

### 本地开发环境

**操作系统**: macOS
**Python 版本**: 3.13.11 (Python 3.14.2 不兼容某些包)
**Node.js 版本**: v25.4.0
**Docker**: 已安装但网络问题（Docker Hub 超时）

### 问题解决

#### 问题 1: Python 3.14 兼容性

**症状**:
```python
# greenlet 和 pydantic-core 编译失败
# 错误: Py 3.14 与某些 C 扩展不兼容
```

**解决**:
```bash
# 使用 Python 3.13 代替
brew install python@3.13
/opt/homebrew/opt/python@3.13/bin/python3.13 -m venv venv
```

**经验**: 次新 Python 版本可能有兼容性问题，使用稳定版本

#### 问题 2: SQLAlchemy 导入错误

**症状**:
```python
# ImportError: cannot import name 'func' from 'sqlalchemy.orm'
```

**解决**:
```python
# SQLAlchemy 2.x 将 func 移至根级别
from sqlalchemy import func  # 正确
# from sqlalchemy.orm import func  # 错误
```

**经验**: 阅读库的变更日志

#### 问题 3: Docker Hub 网络超时

**症状**:
```
failed to do request: Head "https://registry-1.docker.io/v2/..."
net/http: TLS handshake timeout
```

**解决**:
1. 跳过 Docker，本地直接运行
2. 或配置国内镜像源

**经验**: 在中国网络环境下，Docker Hub 访问可能不稳定

---

## 技术决策记录

### 为什么选择 FastAPI 而非 Node.js？

| 因素 | FastAPI | Node.js |
|------|----------|---------|
| 异步爬虫 | 原生 async/await | 需要 async/await 库 |
| 自动文档 | ✅ OpenAPI/Swagger | 需要 Swagger UI |
| 类型安全 | Pydantic 运行时验证 | TypeScript 编译时 |
| Python 生态 | ✅ 爬虫工具成熟 | 可用但不如 Python |
| 决策 | ✅ 选择 FastAPI | |

---

### 为什么选择 Next.js 而非其他框架？

| 因素 | Next.js | Vue | Svelte |
|------|----------|-----|--------|
| SSR/SSG | ✅ 内置 | Nuxt.js (需要额外设置)|
| 生态系统 | ✅ 最大 | 大但不如 React |
| 开发体验 | ✅ 最佳 | 好 |
| 开箱路由 | ✅ 是的 | 需要 vue-router |
| 决策 | ✅ 选择 Next.js | |

---

### 为什么选择 SQLite 而非 PostgreSQL？

| 因素 | SQLite | PostgreSQL |
|------|---------|-----------|
| 简单性 | ✅ 单文件 | 需要服务器进程 |
| 部署 | ✅ 零配置 | 需要安装和配置 |
| 规模 | ✅ 足够 10k 日访客 | 过度但可接受 |
| 加密 | ✅ SQLCipher | 需要额外配置 |
| 决策 | ✅ 选择 SQLite | |

**权衡**: PostgreSQL 更适合 >10k 日访客，但 SQLite 满足当前需求

---

### 数据获取策略

| 数据源 | 方式 | 速率限制 | 刷新频率 |
|--------|------|----------|----------|
| GitHub | REST API | 5000/小时（有 token）| 每小时 |
| npm | REST API | IP 限制 | 每日 |
| PyPI | HTML + API | IP 限制 | 每日 |
| Hugging Face | REST API | 变化 | 每小时 |

**决策**: 混合 API 策略平衡数据新鲜度和速率限制

---

## 测试策略

### 单元测试（本项目未实施）

**建议**:
```python
# FastAPI 自动测试支持
from fastapi.testclient import TestClient
client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
```

### 集成测试（实施）

```bash
# 使用 test.sh 脚本
./scripts/test.sh

# 测试所有 API 端点
- health check
- stats endpoint
- skills endpoints
- source filtering
```

### 手动测试（完成）

- ✅ 前端加载
- ✅ API 响应
- ✅ 数据库创建
- ✅ 环境变量加载

---

## 文档策略

### 文档层次

| 层级 | 目标受众 | 内容 |
|------|----------|------|
| README.md | 用户/开发者 | 快速开始、功能概述 |
| DEPLOYMENT.md | DevOps | 部署步骤、故障排除 |
| UBUNTU_DEPLOYMENT.md | DevOps | 平台特定指南 |
| DESIGN.md | 架构师 | 系统设计、技术选择 |
| PROJECT_SUMMARY.md | 项目经理 | 完成总结 |
| TEST_REPORT.md | QA | 测试结果 |
| 本文档 | 未来开发者 | 经验教训 |

**经验**:
1. ✅ **分层次编写** - 不同受众不同深度
2. ✅ **在创建文档的同时编写** - 不要事后补写
3. ✅ **提供具体示例** - 代码片段、命令

---

## 工作流程优化

### 顺序 vs 并行

| 任务 | 串行耗时 | 并行耗时 | 节省 |
|------|----------|----------|------|
| 探索多个数据源 | 10分钟 | 3分钟 | 70% |
| 构建前端 + 后端 | 5分钟 | 3分钟 | 40% |

**经验**: 尽可能并行执行独立任务

### 批处理操作

```bash
# ✅ 好：并行运行多个独立命令
git status && git diff && git log

# ❌ 差：顺序运行，依赖结果
git status; wait; git diff; wait; git log
```

---

## 代码组织

### 文件结构

```
skill_detector/
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/    # API 路由
│   │   ├── core/   # 配置
│   │   ├── models/ # 数据模型
│   │   └── services/ # 爬虫、调度器
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/          # Next.js 前端
│   ├── app/          # 页面
│   ├── components/   # React 组件
│   ├── lib/         # 工具函数
│   ├── types/       # TypeScript 类型
│   └── Dockerfile
├── nginx/            # 反向代理配置
├── scripts/          # 实用脚本
├── data/            # 数据库存储
├── docker-compose.yml # 编排
└── docs/            # 文档
```

**原则**:
1. 清晰关注分离（后端/前端/基础设施）
2. 按功能组织（api/models/services）
3. 实用脚本集中（scripts/）
4. 文档在根级别（易于访问）

---

## 版本控制最佳实践

### 提交风格

```bash
# 格式: <type>(<scope>): <subject>

feat: add GitHub scraper
fix: resolve SQLAlchemy import error
docs: add deployment guide
refactor: improve error handling
```

### 分支策略

本项目使用 `main`（简单项目）

对于更大项目，考虑：
- `main` - 生产代码
- `develop` - 开发
- `feature/*` - 功能分支
- `hotfix/*` - 紧急修复

### .gitignore 最佳实践

```gitignore
# 环境文件
.env
.env.local

# 数据库
*.db
*.db-shm
*.db-wal
data/

# Python
__pycache__/
*.pyc
venv/

# Node
node_modules/
.next/

# IDE
.vscode/
.idea/
```

---

## 未来改进建议

### 短期（下次项目）

1. **添加单元测试**
   ```python
   # 从第一天开始
   pytest tests/
   ```

2. **使用 CI/CD**
   ```yaml
   # GitHub Actions
   - name: Test
     run: pytest
   - name: Build
     run: docker build
   ```

3. **使用 GitHub Actions 自动更新**
   ```yaml
   # 每日运行爬虫
   schedule:
     - cron: '0 */6 * * *'
   ```

### 长期（规模化）

1. **迁移到 PostgreSQL** - 如果规模 >10k 日访客
2. **添加缓存层** - Redis 用于 API 响应
3. **实现 WebSockets** - 实时更新
4. **添加用户认证** - JWT + OAuth2
5. **微服务架构** - 拆分服务

---

## 关键要点总结

### ✅ 做什么

1. **立即分类请求** - 在行动前
2. **探索使用 `explore`** - 不是手动 grep
3. **并行执行独立任务** - 节省时间
4. **使用 `delegate_task`** - 默认行为
5. **为复杂任务创建 TODO** - 可视化进度
6. **遵循约束** - 不要投机
7. **验证完成** - 证据要求
8. **并行后台探索** - 用完再收集
9. **在创建文档的同时编写** - 不要事后补写
10. **系统化失败处理** - 3 次停止规则

### ❌ 不做什么

1. 不要假设读代码 - 搜索
2. 不要顺序调用探索 - 并行
3. 不要省略所有技能 - 证明省略
4. 不要批处理 TODO - 实时更新
5. 不要类型抑制错误 - `as any`, `@ts-ignore`
6. 不要未请求提交 - 永远不
7. 不要散弹调试 - 系统化方法
8. 不要留代码破坏 - 恢复并咨询
9. 不要过度探索 - 停止条件
10. 不要跳过验证 - 证据要求

---

## 开发环境命令速查

### Python 环境

```bash
# 创建虚拟环境
/opt/homebrew/opt/python@3.13/bin/python3.13 -m venv venv

# 激活
source venv/bin/activate

# 安装依赖
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic

# 运行服务器
uvicorn app.main:app --reload --port 8000
```

### Node.js 环境

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
npm start
```

### Git 操作

```bash
# 初始化
git init

# 添加所有
git add .

# 提交
git commit -m "feat: ..."

# 推送
git push -u origin main
```

### Docker 操作

```bash
# 构建
docker compose build

# 启动
docker compose up -d

# 日志
docker compose logs -f

# 停止
docker compose down
```

---

## 工具和资源

### 开发工具

| 工具 | 用途 | 链接 |
|------|------|------|
| FastAPI | 后端框架 | https://fastapi.tiangolo.com |
| Next.js | 前端框架 | https://nextjs.org |
| SQLAlchemy | ORM | https://sqlalchemy.org |
| Pydantic | 验证 | https://docs.pydantic.dev |
| Tailwind CSS | 样式 | https://tailwindcss.com |
| Docker | 容器化 | https://docs.docker.com |

### 学习资源

| 资源 | 用途 | 链接 |
|--------|------|------|
| FastAPI 教程 | 后端开发 | https://fastapi.tiangolo.com/tutorial |
| Next.js 文档 | 前端开发 | https://nextjs.org/docs |
| REST API 设计 | API 设计 | https://restfulapi.net |
| Docker 最佳实践 | 容器化 | https://docs.docker.com/develop/dev-best-practices |

---

## 结论

这次项目开发过程展示了计划驱动开发的有效性：

1. ✅ **清晰的阶段** - 研究 → 设计 → 实现 → 测试 → 部署
2. ✅ **系统化方法** - 每个阶段有明确目标和成功标准
3. ✅ **委托优先** - 适当任务委托给专业代理
4. ✅ **文档先行** - 边开发边编写文档
5. ✅ **验证驱动** - 证据要求确保质量

**关键收获**: 计划和委托胜过随意编码

---

*最后更新: 2026-02-03*
*下次项目应用: 是的*
