import argparse
import modules.mailer as mail
import modules.setter as set

from os import system

parser = argparse.ArgumentParser(description="Programa entrypoint para o script de envio")

parser.add_argument("-t", "--ticker")
parser.add_argument('-a', "--alert", action='store_true')
parser.add_argument('-m', "--monitor", action='store_true')

args = parser.parse_args()

if args.monitor:
    system("python3 monitor.py")