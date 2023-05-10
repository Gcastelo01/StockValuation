from os import system
from os.path import abspath, exists

class Setter():
    def __init__(self, ticker=None, safety=0.3) -> None:
        self.__ticker = ticker
        self.__safety = safety

    def generate_analysis(self) -> None:
        DATAPATH = abspath('.')
        ENVPATH = DATAPATH + '/.env'

        system(f"echo 'TICKER={self.__ticker}\nSAFETY={self.__safety}' > {DATAPATH}/.env")
        system(f"quarto render {DATAPATH}/assets/Evaluator.ipynb --to pdf --execute --output {self.__ticker}-analysis.pdf")
