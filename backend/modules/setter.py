import asyncio
import logging

from os import system
from os.path import abspath, exists
from datetime import datetime

class Setter():
    def __init__(self, ticker=None, safety=0.3) -> None:
        self.__ticker = ticker
        self.__safety = safety


    async def __get_indicadores(self) -> None:
        try:
            asyncio.create_subprocess_exec('node', 'scripts/')
            
        except Exception as e:
            logging.error(f"Ticker {self.__ticker} não encontrado!")
            raise 
        
    async def generate_analysis(self) -> None:
        DATAPATH = abspath('.')
        INFO = f'TICKER={self.__ticker}\nSAFETY={self.__safety}'

        with open('.env', 'w') as f:
            f.write(INFO)
            f.close()
    
        filename = f"{self.__ticker}-{datetime.now()}-analysis.pdf"
        
        system(f"/usr/local/bin/quarto render ./assets/Evaluator.ipynb --to pdf --execute --output temp/{filename}")
        
        return 'temp/' + filename
