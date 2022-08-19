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

    dfauthors = df['authors'].value_counts()
    dfauthors = dfauthors.head(10)
    dfjournal = df['journal'].value_counts()
    dfjournal = dfjournal.head(10)
    dfyear = df.sort_values('year',ascending=False).head(10)
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

    dft = df.groupby('authors').tail(5).sort_values('year')
    fig3 = px.histogram(dft, x='authors', color='year')
    fig3.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page3 = fig3.to_html(full_html=False, include_plotlyjs='cdn')

    return templates.TemplateResponse("chart.html", {"request":request, "page1":page1, "page2":page2, "page3":page3})