from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# =========================
# GMAIL SMTP CONFIGURATION
# =========================

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


# =========================
# HOME PAGE
# =========================


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# SUBMIT REPORT
# =========================


@app.route("/submit-report", methods=["POST"])
def submit_report():

    name = request.form.get("name")
    date = request.form.get("date")
    project_name = request.form.get("project_name")
    report = request.form.get("report")

    # =========================
    # CREATE EMAIL
    # =========================

    message = MIMEMultipart("alternative")

    message["From"] = SMTP_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = f"Daily Report - {project_name}"

    # =========================
    # EMAIL HTML - SIMPLE & CLEAN
    # =========================

    email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>

<body style="
    margin:0;
    padding:20px;
    font-family:Arial, Helvetica, sans-serif;
    background:#f4f6f9;
">

    <div style="
        max-width:600px;
        margin:0 auto;
        background:#ffffff;
        border-radius:8px;
        border:1px solid #ddd;
        overflow:hidden;
    ">

        <!-- Header -->
        <div style="
            background:#2c3e50;
            padding:20px 25px;
        ">
            <h2 style="
                margin:0;
                color:#ffffff;
                font-size:20px;
                font-weight:600;
            ">
                Daily Report
            </h2>
        </div>

        <!-- Body -->
        <div style="padding:25px;">

            <table style="width:100%;">

                <!-- Name -->
                <tr>
                    <td style="
                        padding:8px 0;
                        color:#555;
                        font-size:14px;
                        width:120px;
                    ">
                        <strong>Name</strong>
                    </td>
                    <td style="
                        padding:8px 0;
                        color:#333;
                        font-size:14px;
                    ">
                        {name}
                    </td>
                </tr>

                <!-- Date -->
                <tr>
                    <td style="
                        padding:8px 0;
                        color:#555;
                        font-size:14px;
                        border-top:1px solid #eee;
                    ">
                        <strong>Date</strong>
                    </td>
                    <td style="
                        padding:8px 0;
                        color:#333;
                        font-size:14px;
                        border-top:1px solid #eee;
                    ">
                        {date}
                    </td>
                </tr>

                <!-- Project -->
                <tr>
                    <td style="
                        padding:8px 0;
                        color:#555;
                        font-size:14px;
                        border-top:1px solid #eee;
                    ">
                        <strong>Project</strong>
                    </td>
                    <td style="
                        padding:8px 0;
                        color:#333;
                        font-size:14px;
                        border-top:1px solid #eee;
                    ">
                        {project_name}
                    </td>
                </tr>

                <!-- Report -->
                <tr>
                    <td style="
                        padding:12px 0 0 0;
                        color:#555;
                        font-size:14px;
                        border-top:1px solid #eee;
                        vertical-align:top;
                    ">
                        <strong>Report</strong>
                    </td>
                    <td style="
                        padding:12px 0 0 0;
                        color:#333;
                        font-size:14px;
                        border-top:1px solid #eee;
                        line-height:1.6;
                    ">
                        {report}
                    </td>
                </tr>

            </table>

        </div>

        <!-- Footer -->
        <div style="
            background:#f8f9fa;
            padding:12px 25px;
            border-top:1px solid #eee;
            text-align:center;
        ">
            <p style="
                margin:0;
                color:#888;
                font-size:12px;
            ">
                This is an automated report.
            </p>
        </div>

    </div>

</body>
</html>
"""

    message.attach(MIMEText(email_body, "html"))

    # =========================
    # SEND EMAIL
    # =========================

    try:

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)

        server.starttls()

        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        server.sendmail(SMTP_EMAIL, RECEIVER_EMAIL, message.as_string())

        server.quit()

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Report Submitted</title>
        </head>

        <body style="
            margin:0;
            padding:60px 20px;
            font-family:Arial, Helvetica, sans-serif;
            text-align:center;
            background:#f4f6f9;
        ">

            <div style="
                max-width:500px;
                margin:auto;
                background:white;
                padding:40px 25px;
                border-radius:8px;
                border:1px solid #ddd;
            ">

                <h2 style="
                    color:#2c3e50;
                    margin-bottom:10px;
                ">
                    ✓ Report Submitted
                </h2>

                <p style="
                    color:#666;
                    margin-bottom:25px;
                ">
                    Your report has been sent successfully.
                </p>

                <a href="/" style="
                    display:inline-block;
                    padding:10px 24px;
                    background:#2c3e50;
                    color:#ffffff;
                    text-decoration:none;
                    border-radius:4px;
                    font-size:14px;
                ">
                    Submit Another Report
                </a>

            </div>

        </body>
        </html>
        """

    except Exception as e:

        print("EMAIL ERROR:", e)

        return (
            """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Email Error</title>
        </head>

        <body style="
            margin:0;
            padding:60px 20px;
            font-family:Arial, Helvetica, sans-serif;
            text-align:center;
            background:#f4f6f9;
        ">

            <div style="
                max-width:500px;
                margin:auto;
                background:white;
                padding:40px 25px;
                border-radius:8px;
                border:1px solid #ddd;
            ">

                <h2 style="
                    color:#c0392b;
                    margin-bottom:10px;
                ">
                    ✗ Failed to Send
                </h2>

                <p style="
                    color:#666;
                    margin-bottom:25px;
                ">
                    Please try again later.
                </p>

                <a href="/" style="
                    display:inline-block;
                    padding:10px 24px;
                    background:#2c3e50;
                    color:#ffffff;
                    text-decoration:none;
                    border-radius:4px;
                    font-size:14px;
                ">
                    Go Back
                </a>

            </div>

        </body>
        </html>
        """,
            500,
        )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)
