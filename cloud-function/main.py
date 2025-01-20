
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main(request):
    # The email address of the Workspace admin to impersonate
    ADMIN_EMAIL = '<REPLACE WITH YOUR WORKSPACE ADMIN EMAIL>'

    # Environment variable for the service account key
    SERVICE_ACCOUNT_KEY = os.getenv("SERVICE_ACCOUNT_KEY")

    if not SERVICE_ACCOUNT_KEY:
        return {"status": "error", "message": "SERVICE_ACCOUNT_KEY not found"}, 500

    # Load credentials from the JSON string in the environment variable
    service_account_info = json.loads(SERVICE_ACCOUNT_KEY)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=[
            'https://www.googleapis.com/auth/admin.directory.user.readonly'
        ]
    )

    # Impersonate the admin user
    delegated_credentials = credentials.with_subject(ADMIN_EMAIL)

    # Build the Admin SDK Directory API service
    service = build('admin', 'directory_v1', credentials=delegated_credentials)

    # Fetch first 100 users in the domain
    try:
        response = service.users().list(customer="my_customer", maxResults=100).execute()
        users = response.get("users", [])
        user_list = [{"id": user["id"], "email": user["primaryEmail"]} for user in users]

        return {"users": user_list}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500