import argparse
import os.path
from os import path
from datetime import datetime
import json
import os
import base64
from json2html import *
import platform

# Houseparty Realm classes containing contacts, chats, timestamp activity and related data of likely interest
usefulitems = ['RealmAuthenticationInfo', 'RealmContact', 'RealmConversation', 'RealmFacemail',
               'RealmHouse', 'RealmHouseAdd', 'RealmHouseItem', 'RealmHouseMessage', 'RealmLocalContact',
               'RealmNote', 'RealmParty', 'RealmPublicUser', 'RealmRelationshipInfo', 'RealmUser',
               'RealmUserSettings']

uname = platform.uname()


# Parsing functions
def facemail(json_file='', outputdir=''):
    # Parses the RealmFacemail class including the thumbnail graphics
    source = open(json_file, 'r', encoding="utf-8")
    json_data = json.load(source)
    os.mkdir(outputdir + '/Facemailthumbs')
    thumbdir = outputdir + '/Facemailthumbs'
    htmlfile = outputdir + '/Facemail.html'
    of = open(htmlfile, 'w', encoding='utf-8')
    of.write(head('Facemail'))
    of.write(
        '<table border="1"><thead><tr><th>id</th><th>mediaID</th><th>thumbnail</th><th>watched</th><th>participants'
        '</th></tr></thead><tbody>')

    for item in json_data['RealmFacemail']:

        # Create thumbnail of base64 encoded data and create .png file named after corresponding mediaID
        mediaid = item['mediaID']
        thumbnail_string = item['thumbnail']
        decoded = base64.b64decode(thumbnail_string)
        new_filename = mediaid + '.png'
        output_path = os.path.join(thumbdir, new_filename)
        output_file = open(output_path, 'wb')
        output_file.write(decoded)
        output_file.close()

        # Get watched boolean and change to string
        if item['watched'] is True:
            watched_status = 'true'
        elif item['watched'] is False:
            watched_status = 'false'
        else:
            watched_status = 'none'

        # Get participants list and change to string
        participants = ', '.join(item['participants'])

        of.write('<tr><td>')
        of.write(item['id'])
        of.write('</td><td>')
        of.write(mediaid)
        of.write("</td><td><img src='Facemailthumbs/")
        of.write(new_filename)
        of.write("'></td><td>")
        of.write(watched_status)
        of.write('</td><td>')
        of.write(participants)
        of.write('</td></tr>')

    of.write('</table>')
    of.write(foot())

    of.close()


def generic(json_file='', outputdir=''):
    # Parses all other Realm classes except RealmFacemail
    source = open(json_file, 'r', encoding="utf-8")
    json_data = json.load(source)
    for item in json_data:
        if item == 'RealmFacemail':
            facemail(json_file, outputdir)
        else:
            output_data = json2html.convert(json=json_data[item])
            htmlfile = outputdir + '/' + item.replace('Realm', '') + '.html'
            of = open(htmlfile, 'w', encoding='utf-8')
            of.write(head(item.replace('Realm', '')))
            of.write(output_data)
            of.write(foot())


def useful(json_file='', outputdir=''):
    # Parses only the classes defined in the usefulitems list
    source = open(json_file, 'r', encoding="utf-8")
    json_data = json.load(source)
    for item in json_data:
        if item in usefulitems:
            if item == 'RealmFacemail':
                facemail(json_file, outputdir)
            else:
                output_data = json2html.convert(json=json_data[item])
                htmlfile = outputdir + '/' + item.replace('Realm', '') + '.html'
                of = open(htmlfile, 'w', encoding='utf-8')
                of.write(head(item.replace('Realm', '')))
                of.write(output_data)
                of.write(foot())


# Report template functions
css = """<style> 
body {
font-family: Arial, Helvetica, sans-serif;
}

table {
border-collapse: collapse;
}

tr:hover {
background-color: #eaeaea;
}

th, td {
padding: 10px;
}

th {
background-color: #b1b1b1;
}

.title {
        font-family: Arial, Helvetica, sans-serif;
        font-weight:bold;
        text-align:center;
    }
</style>"""


def head(title=""): \
        # HTML header data
    return str('<!DOCTYPE html><html><head>' + css + '<title>' + title + '</title></head><body><h1>' + title + '</h1>')


def foot():
    # HTML footer data
    return str('</body></html>')


def data(srcdir, json_file, outputdir, start_time, alltables):
    # Logs local system data for inclusion in the report
    htmldata = """<!DOCTYPE html><html><head>{}<title>HPPO Info</title></head><body><h1><u>H</u>ouse<u>p</u>arty 
    <u>P</u>arsing <u>O</u>utputer
     Info</h1>
    <table border="1">
    <tr><td>Parsed File:</td><td>{}</td></tr>
    <tr><td>Output Directory:</td><td>{}</td></tr>
    <tr><td>Start Time: </td><td>{}</td></tr>
    <tr><td>All Tables Parsed: </td><td>{}</td></tr>
    <tr><td>Operating System:</td><td>{} {}, Version: {}</td></tr>
    <tr><td>Hostname: </td><td>{}</td></tr>
    </table>
    </body></html>""".format(css, json_file, outputdir, start_time.strftime('%Y-%m-%d %H:%M:%S'), alltables,
                             uname.system, uname.release, uname.version, uname.node)
    of = open(srcdir + '/data.html', 'w', encoding='utf-8')
    of.write(htmldata)
    of.close()


def sidebar(srcdir, datadir):
    # Navigation sidebar for report; locates the generated HTML files from parsing and lists them with links
    htmldatahead = """<!DOCTYPE html>
    <html>
    <head>{}</head>
    <title>HPPO Report</title>
    </head>
    <body>
    <pre>
      ,_,
    (0_0)_----------_
   (_____)           |~'
   `-"-"-'           /
     `|__|~-----~|__|
    </pre>
    <h1 class="title">HPPO</h1>
    <ul>
    """.format(css)

    htmldatafoot = """</ul>
    <br/>
    </body>
    </html>
    """

    htmldatalink = """
    <li>
    <a href="data.html" target="data">Parsing Info</a>
    </li>
    <br/>
    """

    of = open(srcdir + '/sidebar.html', 'w', encoding='utf-8')
    of.write(htmldatahead)
    of.write(htmldatalink)

    for root, dirs, files in sorted(os.walk(datadir)):
        for filename in files:
            if filename.endswith('.html'):
                of.write('<li><a href="../data/')
                of.write(filename)
                of.write('" target="data">')
                of.write(filename.replace('.html', ''))
                of.write('</a></li>')

    of.write(htmldatafoot)
    of.close()


def indexpage(resultsdir):
    htmldata = """<!DOCTYPE html>
    <html>
    <head>
    <title>HPPO Report</title>
    </head>
    <frameset cols="250,*">
    <frame name="sidebar" src="src/sidebar.html" scrolling="auto">
    <frame name="data" src="src/data.html" scrolling="auto">
    </frameset>
    </frameset>
    <noframes>
    Your browser does not support frames, and therefore is unable to view this.  Please update your browser.
    If you believe this message to be in error, please contact the program author.
    </noframes>
    </html>"""

    of = open(resultsdir + '/index.html', 'w', encoding='utf-8')
    of.write(htmldata)
    of.close()


def introscreen():
    print("""\n\
  .-''''-. _    
 ('    '  '0)-/)
 '..____..:    \\._
   \\u  u (        '-..------._
   |     /      :   '.        '--.
  .nn_nn/ (      :   '            '\\
 ( '' '' /      ;     .             \\
  ''----' "\\          :            : '.
         .'/                           '.
        / /             H P P O         '.
       /_|       )                     .\\|
         |      /\\                     . '
         '--.__|  '--._  ,            /
                      /'-,          .'
                     /   |        _.' 
                    (____\\       /    
                          \\      \\    
                           '-'-'-'    """)
    print('HPPO - HouseParty Parsing Outputer')


def main():
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

    introscreen()

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
        generic(json_file, datadir)
    else:
        useful(json_file, datadir)

    indexpage(resultsdir)
    data(srcdir, os.path.abspath(json_file), os.path.abspath(outputdir), start_time, alltables)
    sidebar(srcdir, datadir)

    print('Parsing completed at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    main()
