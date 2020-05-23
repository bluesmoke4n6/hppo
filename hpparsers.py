import json
import os
import base64
import hptemplates
from json2html import *

r = hptemplates

usefulitems = ['RealmAuthenticationInfo', 'RealmContact', 'RealmConversation', 'RealmFacemail',
               'RealmHouse', 'RealmHouseAdd', 'RealmHouseMessage', 'RealmLocalContact', 'RealmNote',
               'RealmParty', 'RealmPublicUser', 'RealmRelationshipInfo', 'RealmUser', 'RealmUserSettings']


def facemail(json_file='', outputdir=''):
    source = open(json_file, 'r', encoding="utf-8")
    data = json.load(source)
    os.mkdir(outputdir + '/Facemailthumbs')
    thumbdir = outputdir + '/Facemailthumbs'
    htmlfile = outputdir + '/Facemail.html'
    of = open(htmlfile, 'w', encoding='utf-8')
    of.write(r.head('Facemail'))
    of.write(
        '<table border="1"><thead><tr><th>id</th><th>mediaID</th><th>thumbnail</th><th>watched</th><th>participants'
        '</th></tr></thead><tbody>')

    for item in data['RealmFacemail']:

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
    of.write(r.foot())

    of.close()


def generic(json_file='', outputdir=''):
    source = open(json_file, 'r', encoding="utf-8")
    data = json.load(source)
    for item in data:
        if item == 'RealmFacemail':
            facemail(json_file, outputdir)
        else:
            output_data = json2html.convert(json=data[item])
            htmlfile = outputdir + '/' + item.replace('Realm', '') + '.html'
            of = open(htmlfile, 'w', encoding='utf-8')
            of.write(r.head(item.replace('Realm', '')))
            of.write(output_data)
            of.write(r.foot())


def useful(json_file='', outputdir=''):
    source = open(json_file, 'r', encoding="utf-8")
    data = json.load(source)
    for item in data:
        if item in usefulitems:
            if item == 'RealmFacemail':
                facemail(json_file, outputdir)
            else:
                output_data = json2html.convert(json=data[item])
                htmlfile = outputdir + '/' + item.replace('Realm', '') + '.html'
                of = open(htmlfile, 'w', encoding='utf-8')
                of.write(r.head(item.replace('Realm', '')))
                of.write(output_data)
                of.write(r.foot())
