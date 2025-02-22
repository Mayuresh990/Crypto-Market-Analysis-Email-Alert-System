import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.encoders
import os
import schedule
import time

# Email Configuration (Replace with your own credentials)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your email
SENDER_PASSWORD = "your_app_password"  # Use an app password for security
RECEIVER_EMAIL = "receiver_email@gmail.com"  # Replace with the recipient's email


def send_email(subject, body, filename):
    """Send an email with the crypto report attachment."""
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        email.encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        message.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_crypto_data():
    """Fetch cryptocurrency data from CoinGecko API and send a daily email report."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "inr",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Connection successful! Fetching the data...")

        data = response.json()
        df = pd.DataFrame(data)

        df = df[["id", "current_price", "price_change_percentage_24h", "high_24h", "low_24h", "ath", "atl"]]

        today = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")
        df["timestamp"] = today

        top_negative = df.nsmallest(10, "price_change_percentage_24h")
        top_positive = df.nlargest(10, "price_change_percentage_24h")

        file_name = f"crypto_data_{today}.csv"
        df.to_csv(file_name, index=False)
        print(f"Data saved successfully as {file_name}!")

        subject = f"Daily Crypto Market Report - {today}"
        body = f"""
        <html>
        <head>
            <style>
               table {{
                   width: 100%;
                   border-collapse: collapse;
               }}
               th, td {{
                   border: 1px solid #ddd;
                   padding: 8px;
                   text-align: left;
               }}
               th {{
                   background-color: #4CAF50;
                   color: white;
               }}
            </style>
        </head>
        <body>
            <h2>Daily Crypto Market Report - {today}</h2>
            
            <h3>Top 10 Cryptocurrencies with the Highest Decrease in Price:</h3>
            {top_negative.to_html(index=False, classes='data', header=True, border=1)}
            
            <h3>Top 10 Cryptocurrencies with the Highest Increase in Price:</h3>
            {top_positive.to_html(index=False, classes='data', header=True, border=1)}
            
            <p>Regards,<br>Your Crypto Market Analysis Bot</p>
        </body>
        </html>
        """

        send_email(subject, body, file_name)

    else:
        print(f"Connection failed with error code {response.status_code}")


if __name__ == "__main__":
    get_crypto_data()
    schedule.every().day.at("08:00").do(get_crypto_data)  # Set to your preferred time

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds
