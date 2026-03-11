# SharePoint Video Downloader – Dual Server (FastAPI)

This project allows downloading videos from SharePoint using two separate FastAPI servers:

- **frontend_server.py** → Handles the web interface for submitting SharePoint links.
- **download_server.py** → Handles token authentication and retrieves download URLs.

## Features

- Dual-server architecture (frontend & download server)
- Microsoft OAuth token authentication
- Extracts SharePoint download URLs
- Simple HTML form interface
- Logging for easier debugging

## Requirements

- Python 3.8+
- FastAPI
- Requests
- BeautifulSoup4
- Uvicorn (for running servers)

Install dependencies:

```bash
pip install -r requirements.txt
```
## Configuration

Before running the servers, provide your own Azure AD and SharePoint credentials inside

Required values:

* CLIENT_ID – Azure application client ID
* CLIENT_SECRET – Azure application client secret
* TENANT_ID – Azure tenant ID
* USERNAME – Microsoft account username
* PASSWORD – Microsoft account password

Replace these values inside the scripts.

Example:

```
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"
username = "your_username"
password = "your_password"
```

## Running the Servers

### 1. Start the download server



```
python download_server.py
```

### 2. Start the frontend server

Run the downloader script:

```
python frontend_server.py
```

### 3. Open your browser and go to

http://127.0.0.1:5000

Downloaded files will be saved in the current directory.

Enter the SharePoint link in the form and click Download. The frontend server will send the link to the download server, which will return the direct download URL and redirect the user.

## Notes

* The frontend server acts as a proxy; no files are saved on the server.
* Proper Azure AD permissions are required: Files.Read.All and Sites.Read.All.
* Logging is enabled for both servers for debugging purposes.


## Security Warning

Never publish real credentials in a public repository.

Always remove or replace sensitive information before uploading to GitHub.
