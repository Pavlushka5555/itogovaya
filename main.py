import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import user_router, paint_router, exposition_router
from fastapi.responses import HTMLResponse

app = FastAPI(
    summary="API для картинной галереи",
    version="0.0.1"
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(paint_router, prefix="/paintings", tags=["paintings"])
app.include_router(exposition_router, prefix="/expositions", tags=["expositions"])

app.mount("/static", StaticFiles(directory="site/static"), name="static")

templates = Jinja2Templates(directory="site/templates")


@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


if __name__ == "__main__":
    uvicorn.run(app)
