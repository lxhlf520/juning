# AGENTS.md

## 项目概览
聚宁数据公司门户 —— 互联网数据技术服务公司展示网站。
技术栈：Vue3 + Vite + TailwindCSS（前端）、Python FastAPI + SQLAlchemy（后端）、MySQL/SQLite（数据库）。

## 目录结构
```
/workspace/projects/
├── frontend/              # Vue3 + Vite 前端
│   ├── src/
│   │   ├── api/          # API 请求层 (index.ts)
│   │   ├── components/   # 页面组件
│   │   │   ├── icons/    # SVG 图标组件
│   │   │   ├── NavBar.vue
│   │   │   ├── HeroSection.vue
│   │   │   ├── ServicesSection.vue
│   │   │   ├── CasesSection.vue
│   │   │   ├── AboutSection.vue
│   │   │   ├── ContactSection.vue
│   │   │   └── FooterSection.vue
│   │   ├── composables/  # 可复用逻辑 (useScrollReveal.ts)
│   │   ├── router/       # Vue Router
│   │   ├── views/        # 页面视图
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css     # Tailwind + 自定义样式
│   ├── public/           # 静态资源
│   ├── vite.config.ts    # Vite 配置 (port 5000, proxy /api -> :8000)
│   └── package.json
├── server/                # Python FastAPI 后端
│   ├── main.py           # 入口 (lifespan, CORS, static files)
│   ├── database.py       # SQLAlchemy 引擎 + Session
│   ├── models.py         # ORM 模型 (Service, Case, ContactMessage, CompanyInfo)
│   ├── routes.py         # API 路由
│   ├── seed.py           # 种子数据
│   └── requirements.txt
├── .coze                  # 构建/运行配置
├── DESIGN.md             # 设计规范
└── AGENTS.md             # 本文件
```

## 开发命令
- 前端开发: `cd frontend && pnpm dev` (端口 5000, HMR 端口 6000)
- 后端开发: `python server/main.py` (端口 8000)
- 前端构建: `cd frontend && pnpm build`
- 生产启动: FastAPI 在端口 5000 托管前端静态文件 + API

## 端口规范
- 开发: Vite 前端 5000 / FastAPI 后端 8000 / HMR 6000
- 生产: FastAPI 5000 (API + 静态文件)

## 数据库
- 开发: SQLite (自动创建 company_portal.db)
- 生产: MySQL (通过环境变量 DB_TYPE=mysql, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME 配置)

## API 接口
- GET /api/services - 获取业务服务列表
- GET /api/cases - 获取案例列表
- POST /api/contact - 提交联系表单
- GET /api/company - 获取公司信息

## 代码风格
- Vue3 Composition API + `<script setup>` + TypeScript
- TailwindCSS 4 工具类优先，自定义样式在 style.css
- Python 后端: FastAPI + Pydantic schema + SQLAlchemy ORM
- 组件命名: PascalCase，文件命名: PascalCase.vue
