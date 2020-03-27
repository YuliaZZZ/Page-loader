import argparse
from loader import engine


parser = argparse.ArgumentParser(description='Page loader')  # pragma: no cover
parser.add_argument('site', type=str)      # pragma: no cover
parser.add_argument('-o', '--output', type=str, default='.',
                    help='folder to save page')            # pragma: no cover
args = parser.parse_args()     # pragma: no cover
file_new = engine.page_load(args.site, args.output)      # pragma: no cover
