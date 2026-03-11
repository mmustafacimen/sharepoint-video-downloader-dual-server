from fastapi import FastAPI, Form, HTTPException
import requests
from bs4 import BeautifulSoup
import re
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"

def get_access_token(username, password):
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'offline_access Files.Read.All Files.Read Sites.Read.All',
        'username': username,
        'password': password
    }
    token_r = requests.post(token_url, data=token_data)
    token_r.raise_for_status()
    token_response = token_r.json()
    return token_response['access_token']

def get_download_url(sharepoint_url, access_token):
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(sharepoint_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        script_tags = soup.find_all('script')

        download_url = None
        for script in script_tags:
            script_content = script.string
            if script_content:
                match = re.search(r'downloadUrl":"(.*?)"', script_content)
                if match:
                    download_url = match.group(1).replace('\\u0026', '&')
                    break

        if not download_url:
            raise Exception("Download URL bulunamadı.")

        clean_url = re.sub(r'&.*', '', download_url)
        return clean_url

    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while retrieving data from SharePoint.: {str(e)}")

@app.post("/download")
async def download_file(sharepoint_link: str = Form(...)):
    try:
        logging.info(f"Received SharePoint link: {sharepoint_link}")

        username = "your_username"
        password = "your_password"

        access_token = get_access_token(username, password)
        download_url = get_download_url(sharepoint_link, access_token)

        logging.info(f"Download URL found: {download_url}")
        return download_url

    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download Error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
