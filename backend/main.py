from fastapi import FastAPI
from fastapi.responses import FileResponse


from modules.setter import Setter

app = FastAPI()


@app.get('/{ticker_name}')
async def info_ticker(ticker_name: str):
    sett = Setter(ticker_name)
    file = await sett.generate_analysis()
    
    
    return FileResponse(file)
