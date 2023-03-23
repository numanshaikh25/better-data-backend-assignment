from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
from pathlib import Path
# Initialize FastAPI-Mail instance
conf = ConnectionConfig(
        MAIL_USERNAME = "testcrinitis@gmail.com",
        MAIL_PASSWORD = "cbmunwumrypewhjz",
        MAIL_FROM = "testcrinitis@gmail.com",
        MAIL_PORT = 587,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True

)
fm = FastMail(conf)

async def send_password_reset_email(user_email: str, url: str):
    # Render the email template using Jinja2
    
    template_path = Path(__file__).parent / "templates" /"password_reset_email.html"
    with open(template_path) as f:
            template = Template(f.read())
    html_content = template.render(url=url)
    # Create the email message
    message = MessageSchema(
        subject="Password Reset",
        recipients=[user_email],
        # html=html_content,
        body=f"You have requested to reset your password and here is the link {url}",
        subtype="plain"
    )

    # Send the email
    await fm.send_message(message)
