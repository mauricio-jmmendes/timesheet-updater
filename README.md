# Timesheet Updater

This script automates the process of filling out a Timesheet google sheet for a user-defined week or a specific day. The script uses the Google Sheets and Google Drive APIs, and the `gspread` Python package.

## Prerequisites

1. Python 3 installed on your machine.

2. `pip3` installed on your machine.

3. The following Python packages installed:

    ```bash
    pip3 install gspread oauth2client google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

4. Google Drive and Google Sheets APIs enabled for your Google account.

5. Service Account key file in JSON format (like the `your-service-account-key-file.json` in this repo).

## How to Setup

### Create Google Cloud Project

1. Go to the Google Cloud Console (console.cloud.google.com).

2. Click the project drop-down and select or create the project named "timesheet-updater" (or whatever you choose).

### Create Service Account

1. In the Cloud Console, go to the Service Accounts page.

2. Click "Create Service Account".

3. In the Service account name field, enter a name.

4. Click "Create".

5. Click the "Select a role" field. Under "Quick access", click "Basic", then click "Owner".

6. Click "Continue".

7. Click "Create Key", then choose JSON as the key type.

8. Click "Create". Your new public/private key pair is generated and downloaded to your machine; it serves as the only copy of this key. You are responsible for its safekeeping.

### Share Google Sheet with Service Account

1. Open your JSON key file and look for the "client_email" property. Copy the corresponding email address.

2. Open your Timesheet on Google Sheet, click "Share", and paste the email address. Give it "Editor" access.

## Running the Script

1. Put the JSON key file in the same directory as the Python script.

2. Update the script with your own data (name, spreadsheet name, service account file name).

3. Set an alias for Python 3

    ```bash
    % nano ~/.zshrc
    ```
    ### Add the line below to zsh
    alias python='/usr/local/bin/python3'

    ### And then run
    ```bash
    % touch ~/.zshrc
    ```

4. Run the Python script:

    ```bash
    % python TimesheetUpdater.py
    ```

## Common Errors

### SSL: CERTIFICATE_VERIFY_FAILED

You might see an error message like this if the SSL certificate is not configured properly in your Python environment:

```python
sslc.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1002)
```

To solve this issue, you can point your Python to a specific SSL certificate file. Run the following commands:

```bash
% /Applications/Python\ 3.11/Install\ Certificates.command

 -- pip install --upgrade certifi
Requirement already satisfied: certifi in /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages (2023.5.7)
 -- removing any existing file or link
 -- creating symlink to certifi certificate bundle
 -- setting permissions
 -- update complete
```

#### And then run

```bash
%  cat /usr/local/etc/openssl/certs/combined_cacerts.pem >> /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/certifi/cacert.pem
```

Remember to replace the Python version in the path with your current Python version.
