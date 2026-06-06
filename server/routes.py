"""
API 路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from server.database import get_db
from server.models import Service, Case, ContactMessage, CompanyInfo

router = APIRouter(prefix="/api", tags=["portal"])


# ---------- Pydantic Schemas ----------

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


# ---------- Endpoints ----------

@router.get("/services", response_model=list[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    items = db.query(Service).order_by(Service.sort_order).all()
    return items


@router.get("/cases", response_model=list[CaseOut])
def get_cases(db: Session = Depends(get_db)):
    items = db.query(Case).order_by(Case.sort_order).all()
    return items


@router.post("/contact")
def submit_contact(data: ContactIn, db: Session = Depends(get_db)):
    msg = ContactMessage(
        name=data.name,
        email=data.email,
        phone=data.phone,
        company=data.company,
        message=data.message,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"success": True, "id": msg.id}


@router.get("/contact-messages", response_model=list[ContactMessageOut])
def get_contact_messages(db: Session = Depends(get_db)):
    """查询所有咨询留言，按时间倒序"""
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    # 格式化 created_at
    result = []
    for m in messages:
        result.append(ContactMessageOut(
            id=m.id,
            name=m.name,
            email=m.email,
            phone=m.phone or "",
            company=m.company or "",
            message=m.message,
            created_at=m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else "",
        ))
    return result


@router.delete("/contact-messages/{msg_id}")
def delete_contact_message(msg_id: int, db: Session = Depends(get_db)):
    """删除指定咨询留言"""
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
