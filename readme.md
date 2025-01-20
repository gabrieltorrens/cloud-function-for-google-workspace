# Google Cloud Function: Accessing Google Workspace

This is a demonstration explaining how to access Google Workspace using a GCP Cloud Run Function. We will be using a Workspace admin and domain-wide delegation. This is not the same steps as building a marketplace app to be used by end users.

We will use the Admin SDK to fetch the first 100 users from Workspace. If you are not familiar with cloud computing don't do this until you set up a billing alarm and understand the risks.

I could not find a single page that describes all of the steps to get this working. Google's documentation for this is spread across several pages. And AIs, even Google's, tend to hallucinate when I ask about this. 

---

## Walkthrough

1. **Google Cloud Project**
    - Create a new GCP project (optional)
    - Enable the Admin SDK API
    - We will also be using the Cloud Functions and Secret Manager API, the console UI will prompt you to enable these when you get to that part

2. **Create Service Account and enable Domain-Wide Delegation**
    - Create an IAM service account and generate a JSON key. Download the key.
    - In your service account details page, scroll down to domain-wide delegation and copy the Client ID
    - In Google Workspace, enable domain-wide delegation for the service account. This part can only be done by a Workspace Super Admin.
        - In the Google Admin Console:
        - Go to Security > Access and data contol > API controls > Domain-wide delegation.
        - Add a new client by pasting the Client ID you copied from the GCP console, and grant the following scope: https://www.googleapis.com/auth/admin.directory.user.readonly

3. **Create a new GCP Cloud Run Function**
    - Upload the Service Account JSON Key to Secret Manager
    - Create a new GCP Cloud Run Function using the code in this repo. Replace the ADMIN_EMAIL variable with your Workspace admin email address.
    - The function will be an HTTPS function that requires authentication. The runtime service account will be the service account you created earlier. Add the Secret reference as an environment variable named 'SERVICE_ACCOUNT_KEY'. You should be prompted to give the service account access to the Secret or you may have to do this manually.

4. Verify the Function
    - Test the function from Cloud Shell:
   ```bash
   curl -X GET \
       -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
       https://REGION-YOUR_PROJECT_ID.cloudfunctions.net/FUNCTION_NAME
   ```
    - Check the response to ensure it lists users from the domain.

---

## Why don't you just use GAM?
When I look for this problem online a solution I see, and something I've done in the past, is to use code to wrap around GAM commands. Then put this code in a Cloud VM with a cron trigger. GAM is great but this approach is limited. It doesn't integrate easily with other GCP services and introduces unnecessary overhead. You will also get more flexibilty by working with the APIs directly.