"""
FastAPI 主入口
- 开发环境：仅启动 API 服务（端口 8000），前端由 Vite dev server 提供
- 生产环境：API + 静态文件托管（端口 5000）
"""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# 确保项目根目录在 sys.path 中
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.database import engine, Base
from server.models import Service, Case, ContactMessage, CompanyInfo
from server.routes import router
from server.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：建表 & 种子数据
    Base.metadata.create_all(bind=engine)
    seed_data()
    yield


app = FastAPI(title="聚宁数据门户 API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# 生产环境下托管前端静态文件
ENV = os.getenv("COZE_PROJECT_ENV", "DEV")
if ENV == "PROD":
    static_dir = Path(__file__).parent.parent / "frontend" / "dist"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=(ENV == "DEV"))
