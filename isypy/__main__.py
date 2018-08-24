from isypy import isypy
import argparse
import json


parser = argparse.ArgumentParser(description='Solve the 2D Ising Model.')
parser.add_argument('json_file',  type=str,
                    help='name of the params file in json format')


args = parser.parse_args()
with open(args.json_file, "r") as fin:
    jj_params = json.load(fin)

isypy.run_isypy(jj_params)
