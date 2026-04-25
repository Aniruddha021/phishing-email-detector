import os
import base64
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_latest_emails():

    service = authenticate()

    results = service.users().messages().list(
        userId="me",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:
        txt = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        payload = txt["payload"]
        headers = payload["headers"]

        sender = ""
        subject = ""

        for h in headers:
            if h["name"] == "From":
                sender = h["value"]
            if h["name"] == "Subject":
                subject = h["value"]

        emails.append({
            "sender": sender,
            "subject": subject
        })

    return emails
