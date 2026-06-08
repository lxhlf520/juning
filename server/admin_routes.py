"""
管理后台路由 - 用户管理 + 需求项目管理
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from server.database import get_db
from server.models import User, Project
from server.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_admin
)

router = APIRouter(prefix="/api", tags=["admin"])


# ==================== Pydantic Schemas ====================

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserCreate(BaseModel):
    username: str
    password: str
    display_name: str = ""
    role: str = "staff"  # admin / staff

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class ProjectCreate(BaseModel):
    start_date: Optional[str] = ""
    name: str
    description: Optional[str] = ""
    priority: Optional[str] = ""
    client_type: Optional[str] = ""
    time_dimension: Optional[str] = ""
    detail: Optional[str] = ""
    attachment: Optional[str] = ""
    url: Optional[str] = ""
    quote: Optional[float] = 0
    profit: Optional[float] = 0
    payment_method: Optional[str] = ""
    duration: Optional[str] = ""
    progress: Optional[str] = "待开始"
    is_outsourced: Optional[str] = "否"
    outsourced_to: Optional[str] = ""
    delivery_method: Optional[str] = ""
    is_settled: Optional[str] = "未结算"
    client: Optional[str] = ""

class ProjectUpdate(BaseModel):
    start_date: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    client_type: Optional[str] = None
    time_dimension: Optional[str] = None
    detail: Optional[str] = None
    attachment: Optional[str] = None
    url: Optional[str] = None
    quote: Optional[float] = None
    profit: Optional[float] = None
    payment_method: Optional[str] = None
    duration: Optional[str] = None
    progress: Optional[str] = None
    is_outsourced: Optional[str] = None
    outsourced_to: Optional[str] = None
    delivery_method: Optional[str] = None
    is_settled: Optional[str] = None
    client: Optional[str] = None


# ==================== 认证接口 ====================

@router.post("/auth/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已禁用")
    token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(
        access_token=token,
        user={
            "id": user.id,
            "username": user.username,
            "display_name": user.display_name,
            "role": user.role,
        }
    )

@router.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "display_name": current_user.display_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


# ==================== 用户管理 ====================

@router.get("/users")
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()
    return [{
        "id": u.id,
        "username": u.username,
        "display_name": u.display_name,
        "role": u.role,
        "is_active": u.is_active,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    } for u in users]

@router.post("/users")
def create_user(req: UserCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    if req.role not in ("admin", "staff"):
        raise HTTPException(status_code=400, detail="角色只能是 admin 或 staff")
    user = User(
        username=req.username,
        hashed_password=hash_password(req.password),
        display_name=req.display_name,
        role=req.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": True, "id": user.id}

@router.put("/users/{user_id}")
def update_user(user_id: int, req: UserUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if req.display_name is not None:
        user.display_name = req.display_name
    if req.role is not None:
        if req.role not in ("admin", "staff"):
            raise HTTPException(status_code=400, detail="角色只能是 admin 或 staff")
        user.role = req.role
    if req.is_active is not None:
        user.is_active = req.is_active
    if req.password:
        user.hashed_password = hash_password(req.password)
    db.commit()
    return {"success": True}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return {"success": True}


# ==================== 项目管理 ====================

@router.get("/projects")
def list_projects(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    progress: Optional[str] = Query(None, description="进度筛选"),
    client: Optional[str] = Query(None, description="甲方筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Project)
    if keyword:
        query = query.filter(
            (Project.name.contains(keyword)) |
            (Project.description.contains(keyword)) |
            (Project.client.contains(keyword))
        )
    if progress:
        query = query.filter(Project.progress == progress)
    if client:
        query = query.filter(Project.client == client)
    total = query.count()
    items = query.order_by(Project.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_project_to_dict(p) for p in items],
    }

@router.get("/projects/{project_id}")
def get_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return _project_to_dict(project)

@router.post("/projects")
def create_project(req: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project(
        start_date=req.start_date or "",
        name=req.name,
        description=req.description or "",
        priority=req.priority or "",
        client_type=req.client_type or "",
        time_dimension=req.time_dimension or "",
        detail=req.detail or "",
        attachment=req.attachment or "",
        url=req.url or "",
        quote=req.quote or 0,
        profit=req.profit or 0,
        payment_method=req.payment_method or "",
        duration=req.duration or "",
        progress=req.progress or "待开始",
        is_outsourced=req.is_outsourced or "否",
        outsourced_to=req.outsourced_to or "",
        delivery_method=req.delivery_method or "",
        is_settled=req.is_settled or "未结算",
        client=req.client or "",
        created_by=current_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"success": True, "id": project.id}

@router.put("/projects/{project_id}")
def update_project(project_id: int, req: ProjectUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    update_data = req.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    db.commit()
    return {"success": True}

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    # 只有 admin 或创建者可以删除
    if current_user.role != "admin" and project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此项目")
    db.delete(project)
    db.commit()
    return {"success": True}

@router.get("/projects/stats/summary")
def project_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """项目统计概览"""
    total = db.query(Project).count()
    in_progress = db.query(Project).filter(Project.progress == "正在进行").count()
    completed = db.query(Project).filter(Project.progress == "已完成").count()
    pending = db.query(Project).filter(Project.progress == "待开始").count()
    unsettled = db.query(Project).filter(Project.is_settled == "未结算").count()
    total_quote = sum(p.quote or 0 for p in db.query(Project).all())
    total_profit = sum(p.profit or 0 for p in db.query(Project).all())
    return {
        "total": total,
        "in_progress": in_progress,
        "completed": completed,
        "pending": pending,
        "unsettled": unsettled,
        "total_quote": total_quote,
        "total_profit": total_profit,
    }


def _project_to_dict(p: Project) -> dict:
    return {
        "id": p.id,
        "start_date": p.start_date,
        "name": p.name,
        "description": p.description,
        "priority": p.priority,
        "client_type": p.client_type,
        "time_dimension": p.time_dimension,
        "detail": p.detail,
        "attachment": p.attachment,
        "url": p.url,
        "quote": p.quote,
        "profit": p.profit,
        "payment_method": p.payment_method,
        "duration": p.duration,
        "progress": p.progress,
        "is_outsourced": p.is_outsourced,
        "outsourced_to": p.outsourced_to,
        "delivery_method": p.delivery_method,
        "is_settled": p.is_settled,
        "client": p.client,
        "created_by": p.created_by,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }
