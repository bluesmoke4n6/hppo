import argparse
import os.path
import hpparsers
import hptemplates
from os import path
from datetime import datetime

parser = argparse.ArgumentParser(
    description="HPPO: HouseParty Parsing Outputer: Parses Houseparty JSON data exported from Realm database"
)
parser.add_argument("-j", "--jsonfile", help="Path to Houseparty JSON File")
parser.add_argument("-o", "--outdir", help="Path to output directory")
parser.add_argument("-a", "--alltables", action='store_true', help="Parse ALL tables")
parser.parse_args()

args = parser.parse_args()
alltables = args.alltables

outputdir = args.outdir
json_file = args.jsonfile
start_time = datetime.now()

hptemplates.introscreen()

print('\nStart Time: ' + start_time.strftime('%Y-%m-%d %H:%M:%S'))

resultsdir = outputdir + '/HPPO_Results_' + start_time.strftime('%Y%m%d_%H%M%S')
datadir = resultsdir + '/data'
srcdir = resultsdir + '/src'

if path.exists(outputdir):
    print('Creating output folder: ' + resultsdir)
    os.mkdir(resultsdir)
    os.mkdir(datadir)
    os.mkdir(srcdir)
else:
    os.mkdir(outputdir)
    print('Output directory not found: ' + outputdir)
    print('Creating output directory: ' + outputdir)
    os.mkdir(resultsdir)
    print('Creating output folder: ' + resultsdir)
    os.mkdir(datadir)
    os.mkdir(srcdir)

if alltables:
    print('*Parsing ALL Houseparty Tables*')
    hpparsers.generic(json_file, datadir)
else:
    hpparsers.useful(json_file, datadir)

hptemplates.indexpage(resultsdir)
hptemplates.data(srcdir, os.path.abspath(json_file), os.path.abspath(outputdir), start_time, alltables)
hptemplates.sidebar(srcdir, datadir)

print('Parsing completed at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
