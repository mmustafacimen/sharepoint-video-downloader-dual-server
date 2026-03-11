from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import requests
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/download")
async def send_link(sharepoint_link: str = Form(...)):
    try:
        logging.info(f"Received SharePoint link: {sharepoint_link}")
        download_server_url = "http://localhost:8000/download"
        response = requests.post(download_server_url, data={'sharepoint_link': sharepoint_link})
        response.raise_for_status()
        download_url = response.text.strip('"')
        logging.info(f"Received download URL: {download_url}")
        return RedirectResponse(url=download_url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during download: {str(e)}")
        return f"Download Error: {str(e)}", 500

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
