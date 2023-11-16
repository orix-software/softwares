from io import BytesIO
import pycurl
import json
import os, sys
import pathlib
from os import path
from os.path import exists
import urllib.parse

def get_all_software_from_oric_org():

    print("Retrieve json file from oric.org ...")
    b_obj = BytesIO()
    crl = pycurl.Curl()

    # Set URL value
    crl.setopt(crl.URL, 'http://api.oric.org/0.2/softwares/?sorts=name_software')

    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, b_obj)

    # Perform a file transfer
    crl.perform()

    # End curl session
    crl.close()

    # Get the content stored in the BytesIO object (in byte characters)
    get_body = b_obj.getvalue()

    # Decode the bytes stored in get_body to HTML and print the result
    #print('Output of GET request:\n%s' % get_body.decode('utf8'))

    datastore = json.loads(get_body.decode('utf8'))
    return datastore

def RetrieveSoftwareInTmpFolder(pathFileToDownload, tmpfolderRetrieveSoftware) -> int:

    head, tail = os.path.split(pathFileToDownload)

    # Found software in the folder ? ?
    if  os.path.exists("cache/softwares/"+"/"+tail):
        print (f"Found cache for { pathFileToDownload }")

        f = open("cache/softwares/"+"/"+tail, "rb")
        content=f.read()
        f.close()

        f = open(tmpfolderRetrieveSoftware+"/"+tail, "wb")
        f.write(content)
        f.close()

        return 0

    b_obj_tape = BytesIO()
    crl_tape = pycurl.Curl()

    # Set URL value
    crl_tape.setopt(crl_tape.URL, 'https://cdn.oric.org/games/software/'+urllib.parse.quote(pathFileToDownload))
    print("Not found in cache, download : https://cdn.oric.org/games/software/"+urllib.parse.quote(pathFileToDownload)+" "+tmpfolderRetrieveSoftware+"/"+tail)
    crl_tape.setopt(crl_tape.SSL_VERIFYHOST, 0)

    crl_tape.setopt(crl_tape.SSL_VERIFYPEER, 0)
    # Write bytes that are utf-8 encoded
    crl_tape.setopt(crl_tape.WRITEDATA, b_obj_tape)

    # Perform a file transfer
    try:
        crl_tape.perform()
    except pycurl.error as e:
        # Gestion des exceptions Curl
        print("Erreur Curl :", e)
        return 1
    # End curl session
    crl_tape.close()

    # Get the content stored in the BytesIO object (in byte characters)
    get_body_tape = b_obj_tape.getvalue()

    # Decode the bytes stored in get_body to HTML and print the result
    #print('Output of GET request:\n%s' % get_body.decode('utf8'))

    f = open(tmpfolderRetrieveSoftware+"/"+tail, "wb")
    f.write(get_body_tape)
    f.close()


    f = open("cache/softwares/"+tail, "wb")
    f.write(get_body_tape)
    f.close()
    return 0
