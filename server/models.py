"""
数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, func
from server.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String(500), default="")
    tags = Column(String(500), default="")
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(50), default="")
    company = Column(String(200), default="")
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class CompanyInfo(Base):
    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), default="")
    role = Column(String(20), nullable=False, default="staff")  # admin / staff
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(String(20), default="")           # 开始时间
    name = Column(String(200), nullable=False)             # 项目名称
    description = Column(Text, default="")                # 需求描述
    priority = Column(String(10), default="中")            # 优先级：高/中/低
    client_type = Column(String(20), default="")          # 目标客户端类型
    url = Column(String(500), default="")                  # 网址
    quote = Column(Float, default=0)                        # 报价
    profit = Column(Float, default=0)                       # 利润
    payment_method = Column(String(200), default="")       # 支付方式
    duration = Column(String(200), default="")             # 工期
    progress = Column(String(50), default="待开始")         # 进度
    is_outsourced = Column(String(10), default="否")        # 是否外包
    outsourced_to = Column(String(100), default="")         # 外包人
    delivery_method = Column(String(50), default="")        # 交付方式
    is_settled = Column(String(20), default="未结算")       # 是否结算
    client = Column(String(100), default="")               # 甲方
    remark = Column(Text, default="")                      # 备注
    created_by = Column(Integer, default=0)                 # 创建人ID
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
