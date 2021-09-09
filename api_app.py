from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from scraper import find_data, find_city_id, format_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def search(request: Request):
    return templates.TemplateResponse("search.html", {"request":request, "message":"Search"})

@app.post("/results")
def searched_results(
        request: Request,
        origin: str = Form("origin"),
        destination: str = Form("destination"),
        date: str = Form("date")):
    journeys = format_data(origin, destination, date)

    return templates.TemplateResponse("results.html", {"request":request, "journeys":journeys})


if __name__ == "__main__":
    uvicorn.run(app)