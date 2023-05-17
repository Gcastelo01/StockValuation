import argparse
import modules.mailer as mail
import modules.setter as set

from os import system

parser = argparse.ArgumentParser(description="Programa entrypoint para o script de envio")

parser.add_argument("-t", "--ticker")
parser.add_argument('-a', "--alert", action='store_true')
parser.add_argument('-m', "--monitor", action='store_true')
parser.add_argument('-s', '--setter', action='store_true')
parser.add_argument('-j', "--json", action='store_true')

args = parser.parse_args()

#  Começa o monitor
if args.monitor:
    system("python3 monitor.py")

#  Renderiza o notebook para o ticker passado como argumento
if args.setter:
    s = set.Setter(args.ticker)
    system(f'node ./scripts/getData.js {args.ticker}')
    s.generate_analysis()

#  Busca os dados com a API statusinvest
if args.json:
    INFO = f'TICKER={args.ticker}\nSAFETY=0.3'

    with open('.env', 'w') as f:
        f.write(INFO)
        f.close()

    system(f'node ./scripts/getData.js {args.ticker}')