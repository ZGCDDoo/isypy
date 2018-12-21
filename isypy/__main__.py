from isypy import isypy
import argparse
import yaml


parser = argparse.ArgumentParser(description='Solve the 2D Ising Model.')
parser.add_argument('yaml_file',  type=str,
                    help='name of the params file in json format')


args = parser.parse_args()
with open(args.yaml_file, "r") as fin:
    yy_params = yaml.load(fin)

isypy.run_isypy(yy_params)
