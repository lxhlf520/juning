"""
初始数据种子
"""
from server.database import SessionLocal
from server.models import Service, Case, CompanyInfo

SERVICES_SEED = [
    {
        "title": "数据分析",
        "description": "基于深度学习与统计建模，从海量数据中提取关键洞察，为业务决策提供精准依据。支持用户行为分析、市场趋势预测、运营指标体系搭建等场景。",
        "icon": "chart",
        "sort_order": 1,
    },
    {
        "title": "数据采集",
        "description": "全链路数据采集方案，覆盖网页抓取、API对接、SDK埋点、日志采集等多种方式，确保数据源头的完整性与准确性。",
        "icon": "database",
        "sort_order": 2,
    },
    {
        "title": "Agent 搭建",
        "description": "基于大语言模型构建智能 Agent，实现自动化的数据处理、内容生成、任务编排与多轮交互，让 AI 真正融入业务流程。",
        "icon": "bot",
        "sort_order": 3,
    },
    {
        "title": "App 开发",
        "description": "从需求分析到上架运维的全流程移动应用开发。覆盖 iOS/Android 原生与跨平台方案，注重性能体验与用户增长。",
        "icon": "mobile",
        "sort_order": 4,
    },
    {
        "title": "小程序开发",
        "description": "微信/支付宝/抖音多端小程序定制开发，轻量触达用户场景，助力企业快速获客与业务闭环。",
        "icon": "miniprogram",
        "sort_order": 5,
    },
    {
        "title": "网站开发",
        "description": "企业官网、业务系统、SaaS 平台等全栈 Web 开发。采用现代化技术栈，保障性能、安全与可扩展性。",
        "icon": "web",
        "sort_order": 6,
    },
]

CASES_SEED = [
    {
        "title": "某电商平台用户行为分析系统",
        "description": "为头部电商平台搭建全链路用户行为分析体系，日均处理 2 亿+事件数据，将用户转化率提升 34%，核心功能包括实时漏斗分析、用户分群和智能归因。",
        "image": "/cases/ecommerce.jpg",
        "tags": "数据分析,数据采集",
        "sort_order": 1,
    },
    {
        "title": "智能客服 Agent 系统",
        "description": "基于大语言模型构建多轮对话 Agent，集成知识库检索与工单系统，客户问题自动解决率达 78%，人工客服工作量降低 50%。",
        "image": "/cases/agent.jpg",
        "tags": "Agent搭建,AI应用",
        "sort_order": 2,
    },
    {
        "title": "连锁零售数据中台",
        "description": "为 2000+ 门店的连锁零售品牌搭建统一数据中台，整合 POS、会员、供应链数据，实现经营日报自动化与智能补货建议。",
        "image": "/cases/retail.jpg",
        "tags": "数据分析,数据采集,系统开发",
        "sort_order": 3,
    },
    {
        "title": "智慧社区小程序矩阵",
        "description": "为大型物业管理集团开发覆盖 50+ 社区的微信小程序矩阵，涵盖物业缴费、报修、社区商城等功能，月活用户超 30 万。",
        "image": "/cases/community.jpg",
        "tags": "小程序开发,App开发",
        "sort_order": 4,
    },
]

COMPANY_INFO_SEED = [
    {"key": "company_name", "value": "聚宁数据"},
    {"key": "company_slogan", "value": "聚数成智，宁定未来"},
    {"key": "company_email", "value": "juningdata@163.com"},
    {"key": "company_phone", "value": "17770775849"},
    {"key": "company_address", "value": "深圳市南山区腾讯软件园一期A座2903"},
    {"key": "company_wechat", "value": "juningdata"},
]


def seed_data():
    db = SessionLocal()
    try:
        if db.query(Service).count() == 0:
            for s in SERVICES_SEED:
                db.add(Service(**s))

        if db.query(Case).count() == 0:
            for c in CASES_SEED:
                db.add(Case(**c))

        if db.query(CompanyInfo).count() == 0:
            for ci in COMPANY_INFO_SEED:
                db.add(CompanyInfo(**ci))

        db.commit()
    finally:
        db.close()
