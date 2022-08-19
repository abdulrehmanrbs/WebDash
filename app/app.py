from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import plotly.express as px
import pandas as pd

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def welcome(request: Request, db: Session=Depends(get_db)):
    x=crud.get_sepsis(db)
    df = pd.DataFrame.from_records(x,columns=['authors','year','journal'])
    px.defaults.width = 266
    px.defaults.height = 200

    dft = df.groupby('authors').head(5).sort_values('year')

    fig1 = px.histogram(dft, x='authors', color='year')
    fig1.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

    fig2 = px.histogram(dft, x='year', color='journal')
    fig2.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page2 = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    fig3 = px.histogram(dft, x='authors', color='journal')
    fig3.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page3 = fig3.to_html(full_html=False, include_plotlyjs='cdn')

    dft = df.groupby('authors').tail(5).sort_values('year')

    fig4 = px.histogram(dft, x='authors', color='year')
    fig4.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page4 = fig4.to_html(full_html=False, include_plotlyjs='cdn')

    fig5 = px.histogram(dft, x='year', color='journal')
    fig5.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page5 = fig5.to_html(full_html=False, include_plotlyjs='cdn')

    fig6 = px.histogram(dft, x='authors', color='journal')
    fig6.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page6 = fig6.to_html(full_html=False, include_plotlyjs='cdn')

    return templates.TemplateResponse("chart.html", {"request":request, "page1":page1, "page2":page2, "page3":page3, "page4":page4, "page5":page5, "page6":page6})