import argparse
from loader import engine


parser = argparse.ArgumentParser(description='Page loader')
parser.add_argument('site', type=str)
parser.add_argument('-o', '--output', type=str, default='.', help='folder to save page')
args = parser.parse_args()
file_new = engine.page_load(args.site, args.output)
