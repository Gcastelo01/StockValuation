from os import system
from os.path import abspath, exists

class Setter():
    def __init__(self, ticker=None, safety=0.3) -> None:
        self.__ticker = ticker
        self.__safety = safety

    def generate_analysis(self) -> None:
        DATAPATH = abspath('.')
        INFO = f'TICKER={self.__ticker}\nSAFETY={self.__safety}'

        with open('.env', 'w') as f:
            f.write(INFO)
            f.close()
    
        system(f"quarto render ./assets/Evaluator.ipynb --to pdf --execute --output {self.__ticker}-analysis.pdf")
