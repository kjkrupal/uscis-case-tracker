import boto3
import os
import requests
from bs4 import BeautifulSoup

CASE_NUMBER = os.environ["CASE_NUMBER"]
EMAIL = os.environ["EMAIL"]
CHARSET = "UTF-8"

EMAIL_CONTENT = """
    <html>
        <head></head>
        <body>
            <h1>Your current case status</h1>
            <br><br>
            <p>{status}</p>
        </body>
    </html>
"""

ses_client = boto3.client("ses", region_name="us-east-1")


def handler(event, context):
    url_prefix = "https://egov.uscis.gov/casestatus/mycasestatus.do?language=ENGLISH&caseStatusSearch=caseStatusPage&appReceiptNum="

    page = requests.get(url_prefix + CASE_NUMBER)

    parser = BeautifulSoup(page.content, "html.parser")

    main_case_information = parser.find_all(
        "div", class_="col-lg-12 appointment-sec center"
    )

    current_status = ""

    for info in main_case_information:
        current_status = info.find("h1")

    ses_client.send_email(
        Destination={
            "ToAddresses": [
                EMAIL,
            ]
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": EMAIL_CONTENT.format(status=current_status),
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "USCIS Case Status",
            },
        },
        Source=EMAIL,
    )
