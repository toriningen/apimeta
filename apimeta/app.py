from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from .schemas import MetaResponseScheme
from .scraper import SiteScrapper

app = FastAPI()
# fix nginx issues
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.mount("/static", StaticFiles(directory="apimeta/static"), name="static")
templates = Jinja2Templates(directory="apimeta/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", dict(request=request))


@app.get("/info")
async def info(url: str) -> MetaResponseScheme:
    scrapper = SiteScrapper(url)
    tags = await scrapper.parse()
    return MetaResponseScheme.create(tags)

