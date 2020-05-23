# Template for HTML pages
import platform
import os


uname = platform.uname()

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


def head(title=""):
    return str('<!DOCTYPE html><html><head>' + css + '<title>' + title + '</title></head><body><h1>' + title + '</h1>')


def foot():
    return str('</body></html>')


def data(srcdir, json_file, outputdir, start_time, alltables):
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

    # shutil.copy('resources/hp128.png', srcdir + '/hp128.png')


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
