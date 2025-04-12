from fastapi import FastAPI

from modules.setter import Setter

app = FastAPI()


@app.get('/{ticker_name}')
def info_ticker(ticker_name: str):
    sett = Setter(ticker_name)
    sett.generate_analysis()
    
