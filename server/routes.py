"""
API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from server.database import get_db
from server.models import Service, Case, ContactMessage, CompanyInfo, User, Project
from server.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, require_admin
)

router = APIRouter(prefix="/api", tags=["portal"])


# ==================== Pydantic Schemas ====================

class ServiceOut(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    sort_order: int
    class Config:
        from_attributes = True


class CaseOut(BaseModel):
    id: int
    title: str
    description: str
    image: str
    tags: str
    sort_order: int
    class Config:
        from_attributes = True


class ContactIn(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    company: Optional[str] = ""
    message: str


class CompanyInfoOut(BaseModel):
    key: str
    value: str
    class Config:
        from_attributes = True


class ContactMessageOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    company: str
    message: str
    created_at: Optional[str] = None
    class Config:
        from_attributes = True


# ---------- Auth Schemas ----------

class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    display_name: str
    role: str


class UserCreate(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = ""
    role: Optional[str] = "staff"


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    display_name: str
    role: str
    is_active: bool
    created_at: Optional[str] = None
    class Config:
        from_attributes = True


# ---------- Project Schemas ----------

class ProjectCreate(BaseModel):
    start_date: Optional[str] = ""
    name: str
    description: Optional[str] = ""
    priority: Optional[str] = "中"
    client_type: Optional[str] = ""
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
    remark: Optional[str] = ""


class ProjectUpdate(BaseModel):
    start_date: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    client_type: Optional[str] = None
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
    remark: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    start_date: str
    name: str
    description: str
    priority: str
    client_type: str
    url: str
    quote: float
    profit: float
    payment_method: str
    duration: str
    progress: str
    is_outsourced: str
    outsourced_to: str
    delivery_method: str
    is_settled: str
    client: str
    remark: str
    created_by: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True


# ==================== Portal Endpoints ====================

@router.get("/services", response_model=list[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    items = db.query(Service).order_by(Service.sort_order).all()
    return items


@router.get("/cases", response_model=list[CaseOut])
def get_cases(db: Session = Depends(get_db)):
    items = db.query(Case).order_by(Case.sort_order).all()
    return items


@router.post("/contact")
async def submit_contact(data: ContactIn, db: Session = Depends(get_db)):
    msg = ContactMessage(
        name=data.name, email=data.email, phone=data.phone,
        company=data.company, message=data.message,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    try:
        from server.email_notify import send_contact_notification
        await send_contact_notification(
            name=data.name, email=data.email, phone=data.phone,
            company=data.company, message=data.message,
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"邮件通知发送失败: {e}")
    return {"success": True, "id": msg.id}


@router.get("/contact-messages", response_model=list[ContactMessageOut])
def get_contact_messages(db: Session = Depends(get_db)):
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    result = []
    for m in messages:
        result.append(ContactMessageOut(
            id=m.id, name=m.name, email=m.email, phone=m.phone or "",
            company=m.company or "", message=m.message,
            created_at=m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else "",
        ))
    return result


@router.delete("/contact-messages/{msg_id}")
def delete_contact_message(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    if not msg:
        return {"success": False, "error": "消息不存在"}
    db.delete(msg)
    db.commit()
    return {"success": True}


@router.get("/company", response_model=list[CompanyInfoOut])
def get_company_info(db: Session = Depends(get_db)):
    items = db.query(CompanyInfo).all()
    return items


# ==================== Auth Endpoints ====================

@router.post("/auth/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    token = create_access_token(data={"sub": user.username})
    return TokenOut(
        access_token=token,
        username=user.username,
        display_name=user.display_name,
        role=user.role,
    )


@router.get("/auth/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        display_name=current_user.display_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at.strftime("%Y-%m-%d %H:%M:%S") if current_user.created_at else "",
    )


# ==================== User Management ====================

@router.get("/users", response_model=list[UserOut])
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()
    return [UserOut(
        id=u.id, username=u.username, display_name=u.display_name,
        role=u.role, is_active=u.is_active,
        created_at=u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else "",
    ) for u in users]


@router.post("/users", response_model=UserOut)
def create_user(data: UserCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(
        username=data.username,
        hashed_password=get_password_hash(data.password),
        display_name=data.display_name,
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(
        id=user.id, username=user.username, display_name=user.display_name,
        role=user.role, is_active=user.is_active,
        created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "",
    )


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if data.display_name is not None:
        user.display_name = data.display_name
    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.password:
        user.hashed_password = get_password_hash(data.password)
    db.commit()
    db.refresh(user)
    return UserOut(
        id=user.id, username=user.username, display_name=user.display_name,
        role=user.role, is_active=user.is_active,
        created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "",
    )


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


# ==================== Project Management ====================

@router.get("/projects", response_model=list[ProjectOut])
def list_projects(
    progress: Optional[str] = None,
    client: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Project)
    if progress:
        q = q.filter(Project.progress == progress)
    if client:
        q = q.filter(Project.client.contains(client))
    if search:
        q = q.filter(Project.name.contains(search))
    projects = q.order_by(Project.id.desc()).all()
    return [ProjectOut(
        id=p.id, start_date=p.start_date or "", name=p.name,
        description=p.description or "", priority=p.priority or "中",
        client_type=p.client_type or "", url=p.url or "",
        quote=p.quote or 0, profit=p.profit or 0,
        payment_method=p.payment_method or "", duration=p.duration or "",
        progress=p.progress or "待开始", is_outsourced=p.is_outsourced or "否",
        outsourced_to=p.outsourced_to or "", delivery_method=p.delivery_method or "",
        is_settled=p.is_settled or "未结算", client=p.client or "",
        remark=p.remark or "", created_by=p.created_by or 0,
        created_at=p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else "",
        updated_at=p.updated_at.strftime("%Y-%m-%d %H:%M:%S") if p.updated_at else "",
    ) for p in projects]


@router.post("/projects", response_model=ProjectOut)
def create_project(data: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = Project(**data.model_dump(), created_by=current_user.id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return ProjectOut(
        id=p.id, start_date=p.start_date or "", name=p.name,
        description=p.description or "", priority=p.priority or "中",
        client_type=p.client_type or "", url=p.url or "",
        quote=p.quote or 0, profit=p.profit or 0,
        payment_method=p.payment_method or "", duration=p.duration or "",
        progress=p.progress or "待开始", is_outsourced=p.is_outsourced or "否",
        outsourced_to=p.outsourced_to or "", delivery_method=p.delivery_method or "",
        is_settled=p.is_settled or "未结算", client=p.client or "",
        remark=p.remark or "", created_by=p.created_by or 0,
        created_at=p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else "",
        updated_at=p.updated_at.strftime("%Y-%m-%d %H:%M:%S") if p.updated_at else "",
    )


@router.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="项目不存在")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return ProjectOut(
        id=p.id, start_date=p.start_date or "", name=p.name,
        description=p.description or "", priority=p.priority or "中",
        client_type=p.client_type or "", url=p.url or "",
        quote=p.quote or 0, profit=p.profit or 0,
        payment_method=p.payment_method or "", duration=p.duration or "",
        progress=p.progress or "待开始", is_outsourced=p.is_outsourced or "否",
        outsourced_to=p.outsourced_to or "", delivery_method=p.delivery_method or "",
        is_settled=p.is_settled or "未结算", client=p.client or "",
        remark=p.remark or "", created_by=p.created_by or 0,
        created_at=p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else "",
        updated_at=p.updated_at.strftime("%Y-%m-%d %H:%M:%S") if p.updated_at else "",
    )


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="项目不存在")
    db.delete(p)
    db.commit()
    return {"success": True}


# ==================== Dashboard Stats ====================

@router.get("/dashboard/stats")
def get_dashboard_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total = db.query(Project).count()
    in_progress = db.query(Project).filter(Project.progress == "正在进行").count()
    completed = db.query(Project).filter(Project.progress == "已完成").count()
    pending = db.query(Project).filter(Project.progress == "待开始").count()
    unsettled = db.query(Project).filter(Project.is_settled == "未结算").count()
    total_quote = sum(p.quote or 0 for p in db.query(Project).all())
    return {
        "total": total,
        "in_progress": in_progress,
        "completed": completed,
        "pending": pending,
        "unsettled": unsettled,
        "total_quote": total_quote,
    }
