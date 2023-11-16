# http://api.oric.org/0.2/softwares/

import json
import pycurl
import zipfile
import os, sys
from io import BytesIO
import pathlib
import re
from datetime import date
from os import path
import urllib.parse
from shutil import copyfile

from functions.utils import CreateTargetFolder, RuleLoader, isOric1, isAtmos, isOrix, isRom, removeFrenchChars, getFileExtension, initFolder
from functions.write_db_file import DecimalTo16bits,populateDbFileWithTypeDemo,populateDbFileWithTypeMusic,populateDbFileWithTypeGame,populateDbFileWithTypeUtils,DecimalToBinary,computeVersion,write_db_file_v2, KeyboardMatrix
from functions.get_http_oric_org import get_all_software_from_oric_org, RetrieveSoftwareInTmpFolder

utils_dbv2_str = ""

basic_main_db_str = ""
basic10_main_db_str = ""
game_db_str = ""
game_dbv2_str = ""
music_db_str = ""
demos_db_str = ""
utils_db_str = ""
unsorted_db_str = ""

nb_of_utils_v2 = ""

skipping_list_error = ""
#                       low, high
main_db_table_software = [1,0]
lenAddSoftware = 0
nb_of_games_v2 = 0
start=1

version_bin = "0"
version_bin_v2 = "1"
destroot = "../build/"

# Basic11
dest = "../build/usr/share/basic11/"
destetc = "../build/var/cache/basic11/"

#Basic10
dest_basic10 = "../build/usr/share/basic10/"

# Stratsed
dest_stratsed = "../build/usr/share/stratsed/"
dest_db_stratsed = "../build/var/cache/stratsed/"
destetcstratsed = "../build/var/cache/stratsed/"
stratsed_main_db = "stratsed.db"
number_of_software_stratsed = 0
stratsed_main_db_str = ""


#ftdos
destftdos = "../build/usr/share/ftdos/"
dest_db_ftdos = "../build/var/cache/ftdos/"
destetcftdos = "../build/var/cache/ftdos/"
ftdos_main_db = "ftdos.db"
ftdos_main_db_str = ""
number_of_software_ftdos = 0
ftdos_main_db_str = ""

#Sedoric
destsedoric = "../build/usr/share/sedoric/"
dest_db_sedoric = "../build/var/cache/sedoric/"
destetcsedoric = "../build/var/cache/sedoric/"
sedoric3_main_db = "sedoric3.db"
sedoric3_main_db_str = ""
number_of_software_sedoric = 0

# Roms
destroms = "../build/usr/share/roms/"

destdloppybuilder = "../build/usr/share/fbuilder/"
destmym = "../build/usr/share/mym/"
desthrs = "../build/usr/share/hrs/"
destpt3 = "../build/usr/share/pt3/"
destosid = "../build/usr/share/osid/"

basic_main_db = "basic11.db"
basic_main_db_indexed = "basic11i.db"
basic10_main_db = "basic10.db"
basic10_main_db_indexed = "basic10i.db"

music_dbv2_str = ""
nb_of_music_v2 = 0
demos_dbv2_str = ""

nb_of_demo_v2 = 0

number_of_db_part =1
number_of_software_basic10 = 0
number_of_software_basic11 = 0
basic_games_db = "games.db"
basic_demos_db = "demos.db"
basic_utils_db = "utils.db"
basic_unsorted_db = "unsorted.db"
basic_music_db = "music.db"
basic_games_db_v2 = "games2.db"
basic_demos_db_v2 = "demos2.db"
basic_utils_db_v2 = "utils2.db"
basic_unsorted_db_v2 = "unsortd2.db"
basic_music_db_v2 = "music2.db"



destetc_basic10 = "../build/var/cache/basic10/"
destetc_roms = "../build/etc/systemd/"
roms_banks_cnf = ""
destlauncher = "../build/var/cache/loader/"

skipping_problem_tape_filename = "tape_error.txt"
destloadermd = "../build/usr/share/loader/"
filename_no_support_for_software = "software_error.txt"
tmpfolderRetrieveSoftware = "build/"
list_file_for_md2hlp = ""
nb_of_games = 0
nb_of_unsorted = 0
nb_of_music = 0
nb_of_demo = 0
nb_of_tools = 0
nb_of_roms = 0

nb_of_utils_v2 = 0

def buildDbFileSoftwareSingle(tsoftware, destetc, letter, filenametap8bytesLength, version_bin, rombasic11):

    print("Writting db file : " + destetc + "/" + letter + "/" + filenametap8bytesLength + ".db")
    #ICI
    f = open(destetc+"/" +letter+"/" + filenametap8bytesLength +".db", "wb")
    f.write(DecimalToBinary(version_bin))
    f.write(DecimalToBinary(rombasic11))
    f.write(KeyboardMatrix(tsoftware["fire2_joy"]))
    f.write(KeyboardMatrix(tsoftware["fire3_joy"]))
    f.write(KeyboardMatrix(tsoftware["down_joy"]))
    f.write(KeyboardMatrix(tsoftware["right_joy"]))
    f.write(KeyboardMatrix(tsoftware["left_joy"]))
    f.write(KeyboardMatrix(tsoftware["fire1_joy"]))
    f.write(KeyboardMatrix(tsoftware["up_joy"]))
    f.write(DecimalToBinary(len(tsoftware["name_software"])))
    name_software_bin = bytearray(removeFrenchChars(tsoftware["name_software"]), 'ascii')
    name_software_bin.append(0x00)
    f.write(name_software_bin)
    f.close()

def fileToExecuteTruncateTo8Letters(filename):
    head, tail = os.path.split(filename)
    filenametap =tail.lower().replace(" ", "").replace("-", "").replace("_", "")
    print("Filenametap : " + filenametap)
    print("Split with dot : " + filenametap)
    tcnf = filenametap.split('.')
    filenametapext = tcnf[1]
    filenametapbase = tcnf[0]
    filenametap8bytesLength = filenametapbase[0:8] +"."+filenametapext

    return filenametap8bytesLength.upper()

def buildMdFile(tsoftware, filenametap8bytesLength, dest,letter, download_platform_software):
    name_software = tsoftware["name_software"]
    date_software = tsoftware["date_software"]
    programmer_software = tsoftware["programmer_software"]
    junk_software = tsoftware["junk_software"]
    id_software = tsoftware["id_software"]

    md_software ="#" +removeFrenchChars(tsoftware["name_software"]) +"\n\n"
    tdate_software = date_software.split('-')
    year =tdate_software[0]
    if year == "0000":
        year ="Unknown"
    md_software = md_software+"Release Date : "+year+"\n\n"
    md_software = md_software +"Platform : "
    match = re.search('A', download_platform_software)
    doslash = "no"
    if match:
        md_software = md_software +"Atmos"
        doslash = "yes"
    match = re.search('O', download_platform_software)
    if match:
        if doslash == "yes":
            md_software = md_software +"/"
            md_software = md_software +"Oric-1"
    match = re.search('T', download_platform_software)
    if match:
        if doslash == "yes":
            md_software = md_software + "/"
            md_software = md_software + "Telestrat"
    match = re.search('L', download_platform_software)
    if match:
        if doslash == "yes":
            md_software = md_software + "/"
            md_software = md_software + "Twilighte board joysticks"
    match = re.search('J', download_platform_software)
    if match:
        if doslash == "yes":
            md_software = md_software +"/"
            md_software = md_software +"FTDOS"
    match = re.search('S', download_platform_software)
    if match:
        if doslash == "yes":
            md_software = md_software +"/"
            md_software = md_software +"Sedoric"
    match = re.search('Z', download_platform_software)
    if match:
        if doslash == "yes":
            md_software = md_software + "/"
        md_software = md_software + "Orix"
    md_software =md_software + "\n\n"
    if programmer_software == "":
        md_software = md_software + "Programmer : Unknown\n\n"
    else:
        md_software = md_software + "Programmer : "+removeFrenchChars(programmer_software)+"\n\n"

    md_software = md_software + "Informations : " +removeFrenchChars(junk_software)+"\n\n"
    print("Retrieve comments for software ..." + id_software)

    if os.path.isfile("cache/comments/" + id_software):
        file = open("cache/comments/" + id_software,mode='r')
        # read all lines at once
        list_comment = file.read()
        # close the file
        file.close()
        list_comment = json.loads(list_comment)
        print(f"Fetch cache cache/comments/{id_software}")

    else:

        b_obj = BytesIO()
        crl = pycurl.Curl()

        # Set URL value
        crl.setopt(crl.URL, 'http://api.oric.org/0.2/comments/' + id_software)

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

        f = open("cache/comments/" +id_software, "w")
        f.write(get_body.decode('utf8'))
        f.close()

        list_comment = json.loads(get_body.decode('utf8'))

    #print("List comment"+list_comment)
    if list_comment:
        md_software = md_software+"=== Comments ===\n\n"
        for i in range(len(list_comment)):
            comment=list_comment[i]["comment"]
            md_software=md_software + removeFrenchChars(comment) + "\n"
            md_software=md_software + "------\n\n"

    md=filenametap8bytesLength + ".md"
    file_md_path =dest + "/"+ letter+"/"+md
    f = open(file_md_path, "wb")
    md_software = re.sub(u"\u2013", "-", md_software)
    md_software = re.sub(u"\u2019", "'", md_software)
    md_software = re.sub(u"\u2026", "...", md_software)

    md_software =md_software.replace(r"\r\n", r"\n")
    print(md_software)
    md_bin = bytearray(md_software, 'ascii')
    f.write(md_bin)
    f.close()

    # For loader
    if not os.path.exists(destloadermd + "/"+letter):
        os.mkdir(destloadermd +"/" +letter)

    file_md_path = destloadermd + "/"+ letter+"/"+md
    print(f"Writing md { file_md_path }")
    f = open(file_md_path, "wb")
    md_bin = bytearray(md_software,'ascii')
    f.write(md_bin)
    f.close()

def BuildDsk(tsoftware, platform_software, letter, destpath, destetc, filenametap8bytesLength, tail, tmpfolderRetrieveSoftware, version_bin, rombasic11):
    name_software = tsoftware["name_software"]
    date_software = tsoftware["date_software"]
    programmer_software = tsoftware["programmer_software"]
    junk_software = tsoftware["junk_software"]

    CreateTargetFolder(destpath, destetc,letter)
    print("[DSK]Copying dsk : " + tmpfolderRetrieveSoftware + tail  + " into :"+destpath + "/"+ letter +"/"+filenametap8bytesLength+".dsk" )
    copyfile(tmpfolderRetrieveSoftware+tail,destpath+ "/" +letter+"/"+ filenametap8bytesLength+".dsk" )
    os.remove(tmpfolderRetrieveSoftware + tail)
    if not os.path.exists(destetc + "/"+ letter):
        os.mkdir(destetc+"/" + letter)
    buildMdFile(tsoftware, filenametap8bytesLength, destpath, letter, platform_software)
    buildDbFileSoftwareSingle(tsoftware, destetc,letter, filenametap8bytesLength, version_bin,rombasic11)

def BuildTape(tsoftware, tmpfolderRetrieveSoftware, tail, dest, letter,filenametap8bytesLength,filenametapext,destroot,destetc,download_platform_software,version_bin,rombasic11):
    #Hobbit ROM we copy also the tape file at the root of the sdcard
    print("Copying tape : " + tmpfolderRetrieveSoftware+ tail+" to : "+dest+"/"+letter+"/"+filenametap8bytesLength+"."+filenametapext)

    print("Rom basic id : " + str(rombasic11))
    CreateTargetFolder(dest, destetc, letter)
    copyfile(tmpfolderRetrieveSoftware + tail, dest+"/"+letter+"/"+filenametap8bytesLength+"."+filenametapext)

    # Rom hobbit
    if rombasic11 == "4":
        print("Copy : "  + tmpfolderRetrieveSoftware+tail+" to : "+destroot+"/"+filenametap8bytesLength+"."+filenametapext )
        copyfile(tmpfolderRetrieveSoftware+tail, destroot +"/"+ filenametap8bytesLength+"."+filenametapext )
        # Force to ROM 0 : hobbit ROM
        rombasic11 = 0
    # In oric.org we have roms id to declare if a game is working or not, and if it's
    if rombasic11 != "0" and rombasic11 != "1" and rombasic11 != "2":
        rombasic11 = 1

    if not os.path.exists(destetc + "/" + letter):
        os.mkdir(destetc + "/" + letter)
    print("Writing in db file rom id : ", str(rombasic11))
    buildMdFile(tsoftware, filenametap8bytesLength, dest, letter, download_platform_software)
    buildDbFileSoftwareSingle(tsoftware, destetc, letter, filenametap8bytesLength, version_bin, rombasic11)

def CheckTape(tsoftware, filename, tmpfolderRetrieveSoftware, tail, dest, letter, filenametap8bytesLength, filenametapext, destroot, destetc, download_platform_software, version_bin, rombasic11):
    if filename == "":
        return 1

    if filenametapext == "tap":
        print("Found tape file : " + removeFrenchChars(tsoftware['name_software']) + "Extension : " + filenametapext)
        BuildTape(tsoftware, tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength, filenametapext, destroot, destetc, download_platform_software, version_bin, rombasic11)
        # main db
        return 0

    return 1

def BuildRom(
    tsoftware,
    download_label,
    cnf,
    download_file,
    tmpfolderRetrieveSoftware,
    destpath,
    letter,
    filenametap8bytesLength
    ):

    name_software = tsoftware["name_software"]

    # remove rom in the name
    name_software = name_software.replace(" ROMS","")
    name_software = name_software.replace(" ROM","")

    cnf = cnf +"["+name_software +" ("+download_label+")" +"]"
    cnf = cnf + "\n"
    cnf = cnf +"path=/usr/share/roms/" +letter+"/"+filenametap8bytesLength+".rom"+ "\n"
    print("[ROM] Copying ROM : " + tmpfolderRetrieveSoftware+tail+" into :" +destpath+"/"+letter+"/"+filenametap8bytesLength+".rom" )
    copyfile(tmpfolderRetrieveSoftware +tail, destpath+"/"+letter+"/"+ filenametap8bytesLength+".rom")
    return cnf

def CheckZip(filename):
    extension = filename[-3:].lower()
    if extension == "zip":
        return 0
    return 1

def CheckDsk(
    tsoftware,
    download_software,
    download_platform_software,
    letter,
    destftdos,
    destetcftdos,
    filenametap8bytesLength,
    tail,
    tmpfolderRetrieveSoftware,
    version_bin,
    rombasic11,
    ):


    name_software = tsoftware["name_software"]
    programmer_software = tsoftware["programmer_software"]
    date_software = tsoftware["date_software"]
    junk_software = tsoftware["junk_software"]

    extension = download_software[-3:].lower()
    print("Checkdisk : " + download_software+" ext :"+extension)
    if extension =="dsk":

        match = re.search('J', download_platform_software)

        print("[DSK] download_software : " + download_software+" flags : " +download_platform_software)
        if match:
            # Jasmin
            print ('[DSK] jasmin/ftdos dsk file')
            BuildDsk(tsoftware, download_software, letter, destftdos, destetcftdos, filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,version_bin,rombasic11)
            return 1

        match = re.search('S', download_platform_software)
        if match:
            # Sedoric
            print ('[DSK] Sedoric dsk file')
            BuildDsk(tsoftware, download_software, letter, destsedoric, destetcsedoric,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,version_bin,rombasic11)
            return 2

        # Stratsed ?
        match = re.search('N', download_platform_software)
        if match:
            print ('[DSK] stratsed dsk file')
            BuildDsk(tsoftware, download_software, letter, dest_stratsed, destetcstratsed,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,version_bin,rombasic11)
            return 3

    return 0

def manage_download(tsoftware, download_file, download_platform, download_label, tmpfolderRetrieveSoftware,version_bin, rombasic11,id_download):
    global roms_banks_cnf
    global nb_of_roms
    global skipping_list_error_txt
    global destftdos
    global destetc_basic10
    global dest_basic10
    global destroot
    global destetc
    global number_of_software_basic10
    global basic_main_db_str
    global number_of_software_basic11
    global lenAddSoftware
    global addSoftwareLauncher
    global game_db_str
    global game_dbv2_str
    global nb_of_games_v2
    global nb_of_games
    global utils_db_str
    global nb_of_tools
    global demos_db_str
    global nb_of_demo
    global unsorted_db_str
    global nb_of_unsorted
    global music_db_str
    global nb_of_utils_v2
    global nb_of_music
    global basic10_main_db_str
    global basic11_main_db_str
    global ftdos_main_db_str
    global sedoric3_main_db_str
    global skipping_list_error
    global utils_dbv2_str
    global download_1_high_priority
    global download_2_high_priority
    global download_3_high_priority
    global download_4_high_priority
    global download_5_high_priority
    global download_6_high_priority
    global download_7_high_priority
    global stratsed_main_db_str

    name_software = tsoftware["name_software"]
    id_software = tsoftware["id_software"]
    date_software = tsoftware["date_software"]
    junk_software = tsoftware["junk_software"]
    programmer_software = tsoftware["programmer_software"]
    category_software = tsoftware["category_software"]

    nb_curl_error = 0

    if download_file != "":
        print(f"Download file : { download_file }")
        print(f"[download_file] Retrieve download file { download_file } to { tmpfolderRetrieveSoftware }")

        while (RetrieveSoftwareInTmpFolder(download_file, tmpfolderRetrieveSoftware) == 1):
            nb_curl_error = nb_curl_error + 1 
            if nb_curl_error == 20:
                exit()

        extension = getFileExtension(download_file)
        head, tail = os.path.split(download_file)
        letter = tail[0:1].lower()
        CreateTargetFolder(dest, destetc, letter)

        print("[DOWNLOAD_"+str(id_download)+"] Generating : " + name_software +"/"+id_software)
        filenametap = tail.lower().replace(" ", "").replace("-", "").replace("_", "")
        print("Split with dot : " + filenametap)
        tcnf = filenametap.split('.')
        filenametapext = tcnf[1]
        cnf = tcnf[0] + ".db"
        filenametapbase = tcnf[0]
        filenametap8bytesLength = filenametapbase[0:8]
        filename8plus3 = fileToExecuteTruncateTo8Letters(filenametap)
        skipping_list_error_txt = ""
        print("[DOWNLOAD_" + str(id_download)+"] Filename : " + filenametap+" tail : "+tail+"  file : " +download_file)

        if isOric1(download_platform):
            CreateTargetFolder(dest_basic10, destetc_basic10, letter)

        if isRom(download_platform):
            if filenametapext == "rom":
                CreateTargetFolder(destroms, "", letter)
                roms_banks_cnf = BuildRom(tsoftware, download_label, roms_banks_cnf, download_file,tmpfolderRetrieveSoftware, destroms,letter, filenametap8bytesLength)
                nb_of_roms = nb_of_roms + 1
            else:
                print("[ROM][DOWNLOAD_" + str(id_download)+"] is not a .rom extension")
            return ""

        if CheckZip(download_file) == 0:
            flag = ""
            flag = RuleLoader(download_platform)
            if flag != "":
                skipping_list_error_txt ="[ZIP][DOWNLOAD_" + str(id_download)+"] Skipping download (reason : ZIP) : "+removeFrenchChars(name_software)+"/Flags : "+download_1_platform+" "+id_software+"\n"
                print("[ZIP][DOWNLOAD_" +str(id_download) +"] seems to be a tape file but it's zipped")
            print("[ZIP][DOWNLOAD_" +str(id_download) +"] zip (Skipping) id_software :" +id_software)
            return ""

        typeDsk = CheckDsk(tsoftware, download_file, download_platform, letter, destftdos, destetcftdos, filenametap8bytesLength, tail, tmpfolderRetrieveSoftware, version_bin,rombasic11)
        if typeDsk != 0:
            print("[DSK][DOWNLOAD_"+str(id_download) +"] Id_software:" + id_software)
            addSoftware = filenametap8bytesLength.upper() +';'+ removeFrenchChars(name_software) +';\0'
            if typeDsk == 2:
                sedoric3_main_db_str = sedoric3_main_db_str + addSoftware
                flag = 'S'

            if typeDsk == 1:
                ftdos_main_db_str = ftdos_main_db_str + addSoftware
                flag = 'J'

            if typeDsk == 3:
                stratsed_main_db_str = stratsed_main_db_str + addSoftware
                flag = 'N'

            addSoftware = filenametap8bytesLength.upper() + ';' +removeFrenchChars(name_software)+';'+flag+';\0'
            isGame = populateDbFileWithTypeGame(addSoftwareLauncher, category_software, "DSK")
            if isGame != "":
                game_dbv2_str = game_dbv2_str + addSoftwareLauncher
                nb_of_games_v2 = nb_of_games_v2 + 1

            return ""

        matchRule = 0
        flag = ""
        if CheckTape(tsoftware, download_file, tmpfolderRetrieveSoftware, tail,dest,letter,filenametap8bytesLength,filenametapext,destroot, destetc,download_platform_software, version_bin,rombasic11)==0:

            print("[TAPE][DOWNLOAD_" + str(id_download)+"] Check tape download")
            addSoftware = filenametap8bytesLength.upper() + ';'+removeFrenchChars(name_software) +'\0'
            if isOric1(download_platform):
                basic10_main_db_str = basic10_main_db_str + addSoftware
                BuildTape(tsoftware, tmpfolderRetrieveSoftware, tail, dest_basic10,letter, filenametap8bytesLength,filenametapext,destroot,destetc_basic10,download_platform_software,version_bin,rombasic11)
                print("[TAPE][DOWNLOAD_" +str(id_download)+"][BASIC10] Adding "+ filenametap8bytesLength+" to basic10 command")
                number_of_software_basic10 = number_of_software_basic10 +1

            if isAtmos(download_platform):
                basic_main_db_str = basic_main_db_str + addSoftware
                print("[TAPE][DOWNLOAD_" + str(id_download) +"][BASIC11] Adding "+filenametap8bytesLength+" to basic11 command")
                number_of_software_basic11 = number_of_software_basic11 + 1

            lenAddSoftware += len(addSoftware)
            main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
            flag = RuleLoader(download_platform)

            if download_1_high_priority ==1:
                addSoftwareLauncher = fileToExecuteTruncateTo8Letters(download_file) + ';'+removeFrenchChars(name_software) +';'+flag+';\0'
                matchRule = 1
                print("[TAPE][DOWNLOAD_" +str(id_download)+"][LOADER] Inserting download " + str(id_download)+" for ("+removeFrenchChars(name_software)+") with flags : "+flag)

                isGame = populateDbFileWithTypeGame(addSoftwareLauncher, category_software, "TAPE")
                if isGame != "":
                    game_db_str = game_db_str + addSoftwareLauncher
                    game_dbv2_str = game_dbv2_str + addSoftwareLauncher
                    nb_of_games = nb_of_games + 1
                    nb_of_games_v2 = nb_of_games_v2 + 1

                isUtils = populateDbFileWithTypeUtils(addSoftwareLauncher, category_software, "TAPE")
                if isUtils != "":
                    utils_db_str = utils_db_str + addSoftwareLauncher
                    utils_dbv2_str = utils_dbv2_str + addSoftwareLauncher
                    nb_of_tools = nb_of_tools + 1
                    nb_of_utils_v2 = nb_of_utils_v2 + 1

                if category_software =="6" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_" + str(id_download)+"][LOADER] Add in category dem in loader db")
                    demos_db_str = demos_db_str + addSoftwareLauncher
                    nb_of_demo = nb_of_demo +1

                if category_software=="7" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_" + str(id_download)+"][LOADER] Add in category unsorted in loader db")
                    unsorted_db_str = unsorted_db_str + addSoftwareLauncher
                    nb_of_unsorted = nb_of_unsorted + 1

                # Game from book
                if category_software == "10" and addSoftwareLauncher != "":
                    print("[TAPE][DOWNLOAD_" + str(id_download)+"][LOADER] Add in category music in loader db")
                    music_db_str = music_db_str + addSoftwareLauncher
                    nb_of_music = nb_of_music + 1


initFolder(dest)
initFolder(destetc)
initFolder(dest_basic10)
initFolder(destetc_basic10)
initFolder(destroms)
initFolder(destetc_roms)
initFolder(destlauncher)
initFolder(destftdos)
initFolder(dest_stratsed)
initFolder(destetcstratsed)
initFolder(destetcftdos)
initFolder(destsedoric)
initFolder(destetcsedoric)
initFolder(tmpfolderRetrieveSoftware)
initFolder(destloadermd)
initFolder("cache")
initFolder("cache/comments")
initFolder("cache/softwares")

print(computeVersion())

datastore = get_all_software_from_oric_org()

for i in range(len(datastore)):

    #Use the new datastore datastructure
    id_software = datastore[i]["id"]

    start = 1

    if start == 1:
        tapefile = datastore[i]["download_software"]
        name_software = datastore[i]["name_software"]
        programmer_software = datastore[i]["programmer_software"]
        download_platform_software = datastore[i]["download_platform_software"]
        date_software = datastore[i]["date_software"]
        junk_software = datastore[i]["junk_software"]
        junk_software = removeFrenchChars(junk_software)
        up_joy = datastore[i]["up_joy"]
        down_joy = datastore[i]["down_joy"]
        right_joy = datastore[i]["right_joy"]
        left_joy = datastore[i]["left_joy"]
        fire1_joy = datastore[i]["fire1_joy"]
        fire2_joy = datastore[i]["fire2_joy"]
        fire3_joy = 0
        name_software = name_software.replace("é", "e")
        name_software = name_software.replace("è", "e")
        name_software = name_software.replace("ç", "c")
        name_software = name_software.replace("°", " ")
        name_software = name_software.replace("à", "a")
        name_software = name_software.replace("â", "o")

        programmer_software = programmer_software.replace("é", "e")
        programmer_software = programmer_software.replace("è", "e")
        programmer_software = programmer_software.replace("ç", "c")
        programmer_software = programmer_software.replace("°", " ")
        programmer_software = programmer_software.replace("à", "a")
        programmer_software = programmer_software.replace("ô", "o")
        category_software = datastore[i]["category_software"]
        tsoftware = dict()
        tsoftware["tapefile"] = datastore[i]["download_software"]
        tsoftware['name_software'] = name_software
        tsoftware["programmer_software"] = programmer_software
        tsoftware["download_platform_software"] = datastore[i]["download_platform_software"]
        tsoftware["date_software"] = datastore[i]["date_software"]
        tsoftware["junk_software"] = datastore[i]["junk_software"]
        tsoftware["id_software"] = datastore[i]["id"]

        tsoftware["up_joy"] = datastore[i]["up_joy"]
        tsoftware["down_joy"] = datastore[i]["down_joy"]
        tsoftware["right_joy"] = datastore[i]["right_joy"]
        tsoftware["left_joy"] = datastore[i]["left_joy"]
        tsoftware["fire1_joy"] = datastore[i]["fire1_joy"]
        tsoftware["fire2_joy"] = datastore[i]["fire2_joy"]
        tsoftware["fire3_joy"] = 0
        tsoftware["category_software"] = category_software


        download_1_platform = datastore[i]["platform_software"]
        download_2_platform = datastore[i]["second_download_platform_software"]
        download_3_platform = datastore[i]["download_3_platform"]
        download_4_platform = datastore[i]["download_4_platform"]
        download_5_platform = datastore[i]["download_5_platform"]
        download_6_platform = datastore[i]["download_6_platform"]
        download_7_platform = datastore[i]["download_7_platform"]
        download_8_platform = datastore[i]["download_8_platform"]
        download_9_platform = datastore[i]["download_9_platform"]
        download_10_platform = datastore[i]["download_10_platform"]
        download_11_platform = datastore[i]["download_11_platform"]

        download_1_file = datastore[i]["download_software"]
        download_2_file = datastore[i]["second_download_software"]
        download_3_file = datastore[i]["download_3_path"]
        download_4_file = datastore[i]["download_4_path"]
        download_5_file = datastore[i]["download_5_path"]
        download_6_file = datastore[i]["download_6_path"]
        download_7_file = datastore[i]["download_7_path"]
        download_8_file = datastore[i]["download_8_path"]
        download_9_file = datastore[i]["download_9_path"]
        download_10_file = datastore[i]["download_10_path"]
        download_11_file = datastore[i]["download_11_path"]

        download_1_label = datastore[i]["download_1_label"]
        download_2_label = datastore[i]["download_2_label"]
        download_3_label = datastore[i]["download_3_label"]
        download_4_label = datastore[i]["download_4_label"]
        download_5_label = datastore[i]["download_5_label"]
        download_6_label = datastore[i]["download_6_label"]
        download_7_label = datastore[i]["download_7_label"]
        download_8_label = datastore[i]["download_8_label"]
        download_9_label = datastore[i]["download_9_label"]
        download_10_label = datastore[i]["download_10_label"]
        download_11_label = datastore[i]["download_11_label"]

        joystick_management_state = datastore[i]["joystick_management_state"]

        rombasic11 = datastore[i]["basic11_ROM_TWILIGHTE"]

        if download_1_file != "":
            print(f"########################################## { name_software } : { id_software } #################################################")
            print("[download_1_file] Retrieve download file " +download_1_file+" to : " + tmpfolderRetrieveSoftware)
            if tmpfolderRetrieveSoftware == "":
                print(f"Error { tmpfolderRetrieveSoftware } is empty")
                exit
            RetrieveSoftwareInTmpFolder(download_1_file, tmpfolderRetrieveSoftware)

            extension=download_1_file[-3:].lower()
            head, tail = os.path.split(download_1_file)
            letter=tail[0:1].lower()

            CreateTargetFolder(dest, destetc, letter)

            print(f"Generating : { name_software }/{id_software}")
            filenametap = tail.lower().replace(" ", "").replace("-", "").replace("_", "")
            tcnf = filenametap.split('.')
            filenametapext = tcnf[1]
            cnf = tcnf[0] + ".db"
            filenametapbase = tcnf[0]
            filenametap8bytesLength = filenametapbase[0:8]
            filename8plus3 = fileToExecuteTruncateTo8Letters(filenametap)

            print(f"Filenametap : { filenametap } tail { tail } tape file : { tapefile }")

            if isOric1(download_1_platform):
                CreateTargetFolder(dest_basic10 ,destetc_basic10, letter)

            if isRom(download_1_platform):
                if filenametapext == "rom":
                    CreateTargetFolder(destroms,"",letter)
                    roms_banks_cnf = BuildRom(tsoftware, download_1_label, roms_banks_cnf, download_1_file, tmpfolderRetrieveSoftware, destroms, letter, filenametap8bytesLength)
                    nb_of_roms=nb_of_roms+1
                else:
                    print("[ROM] is not a .rom extension")

            if CheckZip(download_1_file) == 0:
                flag =""
                flag=RuleLoader(download_1_platform)
                if (flag != ""):
                    skipping_list_error = skipping_list_error + "Skipping download (reason : ZIP) : "+removeFrenchChars(name_software)+"/Flags : "+download_1_platform+" "+ id_software+"\n"
                    print("[ZIP] seems to be a tape file but it's zipped")
                print("[ZIP] zip (Skipping) id_software :" + id_software)

            typeDsk = CheckDsk(tsoftware, download_1_file, download_1_platform,letter,destftdos, destetcftdos, filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,version_bin,rombasic11)
            if typeDsk != 0:
                addSoftware = filenametap8bytesLength.upper() + ';' +removeFrenchChars(name_software)+'\0'
                if typeDsk == 1:
                    sedoric3_main_db_str = sedoric3_main_db_str + addSoftware
                if typeDsk == 2:
                    ftdos_main_db_str = ftdos_main_db_str + addSoftware
                print("[DSK] Id_software:" + id_software)
                isGame = populateDbFileWithTypeGame(addSoftwareLauncher, category_software, "SEDORIC")
                if isGame != "":
                    game_dbv2_str = game_dbv2_str + addSoftwareLauncher
                    nb_of_games_v2 = nb_of_games_v2 + 1

            matchRule =0
            flag = ""
            # Download 1

            # Manage priority :
            # Atmos + tape if available is inserted (high priority)
            # Oric-1 + tape lower priority than atmos
            download_1_high_priority = 0
            download_2_high_priority = 0
            download_3_high_priority = 0
            download_4_high_priority = 0

            if (download_1_platform.find('A') != -1 and download_1_platform.find('K') != -1):
                download_1_high_priority = 1
            else:
                if (download_2_platform.find('A') != -1 and download_2_platform.find('K') != -1):
                    download_2_high_priority = 1
                else:
                    # Oric-1
                    if (download_1_platform.find('O') != -1 and download_1_platform.find('K') != -1):
                        download_1_high_priority = 1
                    else:
                        if (download_2_platform.find('O') != -1 and download_2_platform.find('K') != -1):
                            download_2_high_priority=1


            if CheckTape(tsoftware, download_1_file, tmpfolderRetrieveSoftware, tail,dest,letter, filenametap8bytesLength, filenametapext,destroot,destetc,download_platform_software,version_bin,rombasic11)==0:

                print("[TAPE][DOWNLOAD_1] Check tape download 1")
                addSoftware=filenametap8bytesLength.upper() + ';'+removeFrenchChars(name_software) +'\0'
                if isOric1(download_1_platform):
                    basic10_main_db_str = basic10_main_db_str + addSoftware
                    BuildTape(tsoftware, tmpfolderRetrieveSoftware, tail,dest_basic10, letter, filenametap8bytesLength,filenametapext,destroot,destetc_basic10,download_platform_software,version_bin,rombasic11)
                    print(f"[TAPE][DOWNLOAD_1][ORIC1] Adding { filenametap8bytesLength } to basic10 command")
                    number_of_software_basic10 = number_of_software_basic10+1

                if isAtmos(download_1_platform):
                    basic_main_db_str =basic_main_db_str +addSoftware
                    print(f"[TAPE][DOWNLOAD_1][ATMOS] Adding { filenametap8bytesLength } to basic11 command")
                    number_of_software_basic11 = number_of_software_basic11+1

                lenAddSoftware += len(addSoftware)
                main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
                flag=RuleLoader(download_1_platform)

                if download_1_high_priority == 1:
                    addSoftwareLauncher = fileToExecuteTruncateTo8Letters(download_1_file) +';' + removeFrenchChars(name_software) + ';'+flag+';\0'
                    matchRule = 1
                    print("[TAPE][DOWNLOAD_1] Inserting download 1 for (" + removeFrenchChars(name_software)+") with flags : " +flag)

                    isGame = populateDbFileWithTypeGame(addSoftwareLauncher, category_software, "TAPE")
                    if isGame != "":
                        game_db_str = game_db_str + addSoftwareLauncher
                        game_dbv2_str =game_dbv2_str + addSoftwareLauncher
                        nb_of_games = nb_of_games + 1
                        nb_of_games_v2 = nb_of_games_v2 + 1

                    isUtils = populateDbFileWithTypeUtils(addSoftwareLauncher, category_software, "TAPE")
                    if isUtils != "":
                        utils_db_str = utils_db_str + addSoftwareLauncher
                        utils_dbv2_str = utils_dbv2_str + addSoftwareLauncher
                        nb_of_tools = nb_of_tools + 1
                        nb_of_utils_v2 = nb_of_utils_v2 + 1

                    isDemo = populateDbFileWithTypeDemo(addSoftwareLauncher, category_software, "TAPE")
                    if isDemo != "":
                        demos_db_str = demos_db_str + addSoftwareLauncher
                        demos_dbv2_str = demos_dbv2_str + addSoftwareLauncher
                        nb_of_demo = nb_of_demo + 1
                        nb_of_demo_v2 = nb_of_demo_v2 + 1

                    isMusic = populateDbFileWithTypeMusic(addSoftwareLauncher, category_software, "TAPE")
                    if isMusic != "":
                        music_db_str = music_db_str + addSoftwareLauncher
                        music_dbv2_str = music_dbv2_str + addSoftwareLauncher
                        nb_of_music = nb_of_music + 1
                        nb_of_music_v2 = nb_of_music_v2 + 1

                    if category_software == "7" and addSoftwareLauncher !="":
                        unsorted_db_str = unsorted_db_str+addSoftwareLauncher
                        nb_of_unsorted = nb_of_unsorted+1

                else:
                    print("[TAPE][DOWNLOAD_1] Skipping first download trying second download : " + removeFrenchChars(name_software))
                    skipping_list_error = skipping_list_error + "Skipping first download : " + removeFrenchChars(name_software) + "/Flags : " + download_1_platform + " " + id_software+"\n"

            if download_2_file != "":
                extension = download_2_file[-3:].lower()
                head, tail = os.path.split(download_2_file)
                letter = tail[0:1].lower()
                filenametap = tail.lower().replace(" ", "").replace("-", "").replace("_", "")
                print("Split with dot : " + filenametap)
                if not isOrix(download_2_platform):
                    tcnf = filenametap.split('.')
                    filenametapext = tcnf[1]
                    filenametapbase = tcnf[0]
                    filenametap8bytesLength = filenametapbase[0:8]
                    print(f"[download_2_file] Retrieve download file { download_2_file } to : { tmpfolderRetrieveSoftware}")
                    RetrieveSoftwareInTmpFolder(download_2_file, tmpfolderRetrieveSoftware)
                    if not CheckZip(download_1_file) == 0:
                        print(f"Download file 2 : { download_2_file } { tmpfolderRetrieveSoftware }")
                else:
                    print("Orix version found")
                    flag='Z'

                if CheckDsk(tsoftware, download_2_file, download_2_platform, letter, destftdos, destetcftdos,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware, version_bin, rombasic11) != 0:
                    print("[DSK][download_2_file] Id_software:" + id_software)

                if isRom(download_2_platform):
                    if filenametapext == "rom":
                        CreateTargetFolder(destroms, "", letter)
                        roms_banks_cnf = BuildRom(tsoftware, download_2_label, roms_banks_cnf, download_2_file, tmpfolderRetrieveSoftware,destroms, letter,filenametap8bytesLength)
                        nb_of_roms = nb_of_roms + 1
                    else:
                        print("[ROM][DOWNLOAD2] is not a .rom extension")

                if flag == "" and CheckTape(tsoftware, download_2_file, tmpfolderRetrieveSoftware, tail,dest, letter, filenametap8bytesLength,filenametapext,destroot,destetc,download_platform_software,version_bin,rombasic11)==0:
                    addSoftware = filenametap8bytesLength.upper()+';' +removeFrenchChars(name_software)+'\0'
                    if isOric1(download_2_platform):
                        basic10_main_db_str = basic10_main_db_str +addSoftware
                        BuildTape(tsoftware, tmpfolderRetrieveSoftware, tail, dest_basic10,letter, filenametap8bytesLength,filenametapext,destroot,destetc_basic10,download_platform_software,version_bin,rombasic11)
                        print(f"[TAPE][DOWNLOAD_2][ORIC1] Adding (download2) { filenametap8bytesLength } to basic10 command")
                        number_of_software_basic10 = number_of_software_basic10 + 1

                    if isAtmos(download_2_platform):
                        basic_main_db_str = basic_main_db_str +addSoftware
                        print("[TAPE][DOWNLOAD_2][ATMOS] Adding (download2)" + filenametap8bytesLength+"to basic11 command")
                        number_of_software_basic11 =number_of_software_basic11 + 1

                    lenAddSoftware += len(addSoftware)
                    main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
                    flag=RuleLoader(download_2_platform)

                    if download_2_high_priority == 1:
                        print("[TAPE][DOWNLOAD_2] Inserting download 2 in loader db for (" + removeFrenchChars(name_software) +") with flag : "+flag)
                        addSoftwareLauncher= fileToExecuteTruncateTo8Letters(download_2_file)+';'+ removeFrenchChars(name_software) +';'+flag+';\0'
                        matchRule =1

                        isGame = populateDbFileWithTypeGame(addSoftwareLauncher, category_software, "TAPE")
                        if isGame != "":
                            game_db_str = game_db_str + addSoftwareLauncher
                            game_dbv2_str = game_dbv2_str + addSoftwareLauncher
                            nb_of_games = nb_of_games + 1
                            nb_of_games_v2 = nb_of_games_v2 + 1

                        isUtils = populateDbFileWithTypeUtils(addSoftwareLauncher, category_software, "TAPE")
                        if isUtils != "":
                            utils_db_str = utils_db_str + addSoftwareLauncher
                            utils_dbv2_str = utils_dbv2_str + addSoftwareLauncher
                            nb_of_tools = nb_of_tools + 1
                            nb_of_utils_v2 = nb_of_utils_v2 + 1

                        isDemo = populateDbFileWithTypeDemo(addSoftwareLauncher, category_software, "TAPE")
                        if isDemo != "":
                            demos_db_str = demos_db_str + addSoftwareLauncher
                            demos_dbv2_str = demos_dbv2_str + addSoftwareLauncher
                            nb_of_demo = nb_of_demo + 1
                            nb_of_demo_v2 = nb_of_demo_v2 + 1

                        isMusic = populateDbFileWithTypeMusic(addSoftwareLauncher, category_software, "TAPE")
                        if isMusic != "":
                            music_db_str = music_db_str + addSoftwareLauncher
                            music_dbv2_str = music_dbv2_str + addSoftwareLauncher
                            nb_of_music = nb_of_music + 1
                            nb_of_music_v2 = nb_of_music_v2 + 1

                        if category_software == "7" and addSoftwareLauncher !="":
                            unsorted_db_str = unsorted_db_str +addSoftwareLauncher
                            nb_of_unsorted = nb_of_unsorted+1

                    else:
                        print("Skipping second download, not .tap file found : "  + removeFrenchChars(name_software))
                        skipping_list_error =skipping_list_error+"Skipping second download : " + removeFrenchChars(name_software)+"/Flags : "+download_2_platform+" "+id_software+"\n"

                    if download_1_high_priority == 0 and download_2_high_priority == 0:
                        print("!!!Error!!! No compatible support found for : " + removeFrenchChars(name_software))

            manage_download(tsoftware, download_3_file, download_3_platform, download_3_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,3)
            manage_download(tsoftware, download_4_file, download_4_platform, download_4_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,4)
            manage_download(tsoftware, download_5_file, download_5_platform, download_5_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,5)
            manage_download(tsoftware, download_6_file, download_6_platform, download_6_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,6)
            manage_download(tsoftware, download_7_file, download_7_platform, download_7_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,7)
            manage_download(tsoftware, download_8_file, download_8_platform, download_8_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,8)
            manage_download(tsoftware, download_9_file, download_9_platform, download_9_label, tmpfolderRetrieveSoftware,version_bin, rombasic11,9)
            manage_download(tsoftware, download_10_file, download_10_platform, download_10_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,10)
            manage_download(tsoftware, download_11_file, download_11_platform, download_11_label, tmpfolderRetrieveSoftware, version_bin, rombasic11,11)

EOF=0xFF
print("Write basic11 db" + str(number_of_software_basic11))
f = open(destetc +"/" + basic_main_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic_main_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic10 db/nb : " + str(number_of_software_basic10))
f = open(destetc_basic10 +"/" + basic10_main_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic10_main_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()


print("Write stratsed db/nb : " + str(number_of_software_stratsed))
f = open(destetcstratsed + "/" + stratsed_main_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(stratsed_main_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

#print(main_db_table_software)
# indexed
f = open(destetc+"/" + basic_main_db_indexed, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic_main_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

# V0 loader

print("Write basic_games_db/nb : " + str(nb_of_games))
f = open(destlauncher+"/" + basic_games_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_games))
f.write(bytearray(game_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_demos_db/nb : " + str(nb_of_demo))
f = open(destlauncher+"/" + basic_demos_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_demo))
f.write(bytearray(demos_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_utils_db/nb : " + str(nb_of_tools))
f = open(destlauncher+"/" + basic_utils_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_tools))
f.write(bytearray(utils_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_unsorted_db")
f = open(destlauncher+"/" + basic_unsorted_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_unsorted))
f.write(bytearray(unsorted_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_music_db/nb : " + str(nb_of_music))
f = open(destlauncher+"/"+ basic_music_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_music))
f.write(bytearray(music_db_str, 'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write roms/nb : " + str(nb_of_roms))
f = open(destetc_roms + "/bankstmp.cnf", "wb")
# Remove the last byte which contains \n
f.write(bytearray(roms_banks_cnf[:-1], 'ascii'))
f.close()

games_number_of_db_part = 1
write_db_file_v2("Write games_db/nb v2 : .db ", nb_of_games_v2, games_number_of_db_part, destlauncher + "/" + basic_games_db_v2, game_dbv2_str)

demos_number_of_db_part = 1
write_db_file_v2("Write demos_db/nb v2 : .db ", nb_of_demo_v2, demos_number_of_db_part, destlauncher + "/" + basic_demos_db_v2, demos_db_str)

utils_number_of_db_part = 1
write_db_file_v2("Write utils_db/nb v2 : .db ", nb_of_utils_v2, utils_number_of_db_part, destlauncher + "/" +basic_utils_db_v2, utils_db_str)

# unsorted_number_of_db_part = 1
# write_db_file_v2("Write unsorted_db/nb v2 : .db ", nb_of_unsorted_v2, unsorted_number_of_db_part, destlauncher + "/" +basic_unsorted_db_v2, unsorted_db_str)

music_number_of_db_part = 1
write_db_file_v2("Write basic_music_db/nb v2 : .db ", nb_of_music_v2, music_number_of_db_part,destlauncher + "/"+ basic_music_db_v2, music_db_str)

