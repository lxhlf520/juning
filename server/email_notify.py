"""邮件通知工具模块"""

import os
import logging
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from dotenv import load_dotenv
import aiosmtplib

# 加载 .env 文件
load_dotenv(Path(__file__).parent / ".env")

logger = logging.getLogger(__name__)

# SMTP 配置（通过环境变量读取，.env 文件已包含授权码）
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.163.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "juningdata@163.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # 163 邮箱授权码
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "juningdata@163.com")


async def send_contact_notification(
    name: str,
    email: str,
    phone: Optional[str] = None,
    company: Optional[str] = None,
    message: str = "",
):
    """发送咨询通知邮件"""
    if not SMTP_PASSWORD:
        logger.warning("SMTP_PASSWORD 未配置，跳过邮件通知")
        return

    subject = f"【聚宁数据】新咨询 - {name}"

    # 构建邮件正文
    body_lines = [
        "<div style='font-family: sans-serif; max-width: 600px; margin: 0 auto;'>",
        "<h2 style='color: #06b6d4; border-bottom: 2px solid #06b6d4; padding-bottom: 8px;'>新的客户咨询</h2>",
        "<table style='width: 100%; border-collapse: collapse;'>",
    ]

    fields = [
        ("姓名", name),
        ("邮箱", email),
        ("电话", phone or "未填写"),
        ("公司", company or "未填写"),
    ]

    for label, value in fields:
        body_lines.append(
            f"<tr>"
            f"<td style='padding: 8px 12px; border: 1px solid #e2e8f0; background: #f8fafc; font-weight: 600; width: 80px;'>{label}</td>"
            f"<td style='padding: 8px 12px; border: 1px solid #e2e8f0;'>{value}</td>"
            f"</tr>"
        )

    body_lines.append("</table>")
    body_lines.append(
        f"<h3 style='color: #1e293b; margin-top: 16px;'>咨询内容</h3>"
    )
    body_lines.append(
        f"<div style='padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; line-height: 1.7;'>{message}</div>"
    )
    body_lines.append(
        "<p style='color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 12px;'>"
        "此邮件由聚宁数据官网自动发送，请勿直接回复。</p>"
    )
    body_lines.append("</div>")

    html_body = "".join(body_lines)

    # 构建邮件
    msg = MIMEMultipart("alternative")
    msg["From"] = f"聚宁数据官网 <{SMTP_USER}>"
    msg["To"] = NOTIFY_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        if SMTP_USE_TLS:
            await aiosmtplib.send(
                msg,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                use_tls=True,
            )
        else:
            await aiosmtplib.send(
                msg,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                start_tls=True,
            )
        logger.info(f"通知邮件已发送至 {NOTIFY_EMAIL}")
    except Exception as e:
        logger.error(f"邮件发送失败: {e}")
