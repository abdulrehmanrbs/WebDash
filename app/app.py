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
    px.defaults.width = 800
    px.defaults.height = 600

    authors10 = df['authors'].value_counts().reset_index().head(10)
    fig1 = px.histogram(authors10, x='index', y='authors')
    fig1.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

    journals10 = df['journal'].value_counts().reset_index().head(10)
    fig2 = px.histogram(journals10, x='index', y='journal')
    fig2.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page2 = fig2.to_html(full_html=False, include_plotlyjs='cdn')
    
    authors10_journals = df.loc[df['authors'].isin(authors10['index']),'journal'].value_counts().reset_index().head(10)
    fig3 = px.histogram(authors10_journals, x='index', y='journal')
    fig3.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page3 = fig3.to_html(full_html=False, include_plotlyjs='cdn')

    authors10_yrs = df.loc[(df['year'] >= 2017),'authors'].value_counts().reset_index().head(10)
    fig4 = px.histogram(authors10_yrs, x='index', y='authors')
    fig4.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page4 = fig4.to_html(full_html=False, include_plotlyjs='cdn')

    journals10_yrs = df.loc[(df['year'] >= 2017),'journal'].value_counts().reset_index().head(10)
    fig5 = px.histogram(journals10_yrs, x='index', y='journal')
    fig5.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page5 = fig5.to_html(full_html=False, include_plotlyjs='cdn')
    
    journals_recent_yrs = df.loc[(df['year'] >= 2019),'journal'].value_counts().reset_index().head(25)
    fig6 = px.pie(journals_recent_yrs, names='index', values='journal')
    fig6.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    page6 = fig6.to_html(full_html=False, include_plotlyjs='cdn')

    return templates.TemplateResponse("chart.html", {"request":request, "page1":page1, "page2":page2, "page3":page3, "page4":page4, "page5":page5, "page6":page6})