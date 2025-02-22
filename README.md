# Crypto Market Analysis & Email Alert System  

## Project Overview  
This project fetches real-time cryptocurrency data, analyzes price changes, and sends daily email reports with the top 10 highest and lowest price changes in the last 24 hours. The system is automated using Python, CoinGecko API, and an email-sending module to provide market insights.  

## Files in the Repository  
- app.py - Main Python script for fetching data, processing insights, and sending email alerts.  
- crypto_data_YYYY-MM-DD.csv - Sample output CSV file storing cryptocurrency data.  
- README.md - Project documentation.  
- CHANGELOG.md - Record of updates and improvements.  
- LICENSE.md - Usage rights for this project.  

## Key Features  
- Fetches real-time cryptocurrency prices using CoinGecko API.  
- Identifies top 10 gainers and losers based on 24-hour percentage price change.  
- Generates and saves data in a CSV file.  
- Automatically sends a detailed email report with an attached CSV file.  
- Runs daily at a scheduled time using the schedule module.  

## Tools and Technologies Used  
- Python - Data processing and automation.  
- CoinGecko API - Real-time cryptocurrency data.  
- Pandas - Data processing and filtering.  
- Schedule - Automating daily execution.  
- SMTP (smtplib) - Sending email alerts.  

## Installation and Usage  
1. Install dependencies:  
   ```bash
   pip install requests pandas schedule
