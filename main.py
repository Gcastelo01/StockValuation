import argparse
import modules.mailer as mail
import modules.setter as set

parser = argparse.ArgumentParser(description="Programa entrypoint para o script de envio")

parser.add_argument("-t", "--ticker", required=True)
parser.add_argument('-a', "--alert", action='store_true')

args = parser.parse_args()

ss = set.Setter(args.ticker, 0.3)

ss.generate_analysis()

# m = mail.Mailer(args.ticker,