"""
初始数据种子
"""
from server.database import SessionLocal
from server.models import Service, Case, CompanyInfo, User, Project

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

PROJECTS_SEED = [
    {"start_date": "", "name": "财新网", "description": "文章内容、评论、AI提问选项", "priority": "低", "client_type": "web", "quote": 0, "progress": "待开始", "is_outsourced": "否", "delivery_method": "数据交付", "is_settled": "未结算", "client": "高博"},
    {"start_date": "", "name": "startmaker", "description": "循环采集用户信息、作品信息、评论信息", "priority": "低", "client_type": "app", "quote": 1800, "progress": "正在进行", "is_outsourced": "否", "delivery_method": "数据交付", "is_settled": "未结算", "client": "高博", "duration": "截至到25日完成上线测试"},
    {"start_date": "2026-02-20", "name": "分布式PG数据库平台搭建", "description": "", "priority": "高", "quote": 1500, "progress": "已完成", "is_outsourced": "否", "delivery_method": "平台交付", "is_settled": "未结算", "client": "高博"},
    {"start_date": "2026-02-20", "name": "数据迁移", "description": "", "priority": "高", "quote": 1000, "progress": "已完成", "is_outsourced": "否", "delivery_method": "平台交付", "is_settled": "未结算", "client": "高博"},
    {"start_date": "2026-03-20", "name": "X", "description": "网站会不定时更新，一旦更新之后，我们就拿到这个帖子，然后每隔5分钟，抓一遍这个帖子的转赞评数量", "priority": "高", "client_type": "web", "quote": 2000, "progress": "正在进行", "is_outsourced": "是", "delivery_method": "代码交付", "is_settled": "未结算", "client": "高博", "payment_method": "前期30%、项目完成60%、一周内运行没问题支付剩余尾款"},
    {"start_date": "2026-03-19", "name": "营销2.0 爬虫", "description": "需每月5号、20号分别导出低保五保用户明细与民政局提供的名单匹配出新增和取消的每月进行动态更新，制作成exe可执行程序", "priority": "高", "client_type": "web", "quote": 800, "progress": "已完成", "is_outsourced": "否", "delivery_method": "工具交付", "is_settled": "未结算", "client": "高博"},
    {"start_date": "2026-03-22", "name": "glassdoor", "description": "补充截至到现在的公司评论信息", "priority": "高", "client_type": "web", "quote": 4000, "progress": "已完成", "is_outsourced": "否", "delivery_method": "数据交付", "is_settled": "未结算", "client": "高博"},
    {"start_date": "2026-04-02", "name": "天气网站", "description": "更新数据", "priority": "高", "client_type": "web", "quote": 500, "progress": "已完成", "is_outsourced": "否", "delivery_method": "数据交付", "is_settled": "未结算", "client": "高博"},
    {"start_date": "", "name": "google map", "description": "采集google地图中商家信息", "priority": "高", "client_type": "web", "quote": 0, "progress": "待开始", "is_outsourced": "否", "client": "高博"},
    {"start_date": "2026-05-07", "name": "历史天气预报数据", "description": "", "priority": "中", "quote": 1300, "progress": "正在进行", "is_outsourced": "否", "is_settled": "已结算", "client": "门老师", "payment_method": "代理另算（目前先开并发5个ip,测试）"},
    {"start_date": "2026-05-10", "name": "微博数据监控", "description": "", "priority": "中", "progress": "待开始", "is_outsourced": "否", "client": "门老师"},
    {"start_date": "2026-05-20", "name": "wall street journal", "description": "", "priority": "高", "progress": "正在进行", "is_outsourced": "否", "client": "高博", "duration": "本月完成代码上线采集工作", "remark": "需要交接"},
    {"start_date": "2026-05-20", "name": "daily mail", "description": "", "priority": "高", "progress": "正在进行", "is_outsourced": "否", "client": "高博", "duration": "本月完成代码上线采集工作", "remark": "需要交接"},
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

        # 默认管理员账号
        if db.query(User).count() == 0:
            from server.auth import hash_password
            db.add(User(
                username="admin",
                hashed_password=hash_password("admin123"),
                display_name="管理员",
                role="admin",
                is_active=True,
            ))

        # 示例项目数据
        if db.query(Project).count() == 0:
            for p in PROJECTS_SEED:
                db.add(Project(**p))

        db.commit()
    finally:
        db.close()
