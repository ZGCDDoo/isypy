from isypy import isypy
import argparse


parser = argparse.ArgumentParser(description='Solve the 2D Ising Model.')
parser.add_argument('temperature',  type=float,
                    help='temperature in units of J')

parser.add_argument('Lx', type=int,
                    help='linear length')

args = parser.parse_args()

isypy.run_isypy(args.temperature, args.Lx)
