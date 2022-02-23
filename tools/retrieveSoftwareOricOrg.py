# http://api.oric.org/0.2/softwares/

import json
import pycurl
import zipfile
import os, sys
from io import BytesIO 
import pathlib
import re
from datetime import date




from shutil import copyfile

version_bin="0"
version_bin_v2="1"
destroot="../build/"
dest="../build/usr/share/basic11/"
dest_basic10="../build/usr/share/basic10/"

destftdos="../build/usr/share/ftdos/"
destsedoric="../build/usr/share/sedoric/"
destroms="../build/usr/share/roms/"
destdloppybuilder="../build/usr/share/fbuilder/"
destmym="../build/usr/share/mym/"
desthrs="../build/usr/share/hrs/"
destpt3="../build/usr/share/pt3/"
destosid="../build/usr/share/osid/"

basic_main_db="basic11.db"
basic_main_db_indexed="basic11i.db"

basic10_main_db="basic10.db"
basic10_main_db_indexed="basic10i.db"

number_of_db_part=1

number_of_software_basic10=0
number_of_software_basic11=0
basic_games_db="games.db"
basic_demos_db="demos.db"
basic_utils_db="utils.db"
basic_unsorted_db="unsorted.db"
basic_music_db="music.db"

basic_games_db_v2="games2.db"
basic_demos_db_v2="demos2.db"
basic_utils_db_v2="utils2.db"
basic_unsorted_db_v2="unsortd2.db"
basic_music_db_v2="music2.db"

destetc="../build/var/cache/basic11/"
destetc_basic10="../build/var/cache/basic10/"
destetc_roms="../build/etc/systemd/"
roms_banks_cnf=""

destlauncher="../build/var/cache/loader/"
destetcftdos="../build/var/cache/ftdos/"
destetcsedoric="../build/var/cache/sedoric/"

skipping_problem_tape_filename="tape_error.txt"

 

filename_no_support_for_software="software_error.txt"

tmpfolderRetrieveSoftware="build/"
list_file_for_md2hlp=""
nb_of_games=0
nb_of_unsorted=0
nb_of_music=0
nb_of_demo=0
nb_of_tools=0
nb_of_roms=0

def computeVersion():
   # for m in range(1, 13):
    today = date.today()
    month=int(today.strftime("%m"))
    quarter=str(((month*3)//10)+1)
    
    strversion = today.strftime("%Y."+quarter+".%m.%d")
    return strversion

def buildDbFileSoftwareSingle(destetc,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy):
    print("Writting db file : "+destetc+"/"+letter+"/"+filenametap8bytesLength+".db")
    f = open(destetc+"/"+letter+"/"+filenametap8bytesLength+".db", "wb")
    f.write(DecimalToBinary(version_bin))
    f.write(DecimalToBinary(rombasic11))
    f.write(KeyboardMatrix(fire2_joy))
    f.write(KeyboardMatrix(fire3_joy))            
    f.write(KeyboardMatrix(down_joy))
    f.write(KeyboardMatrix(right_joy))
    f.write(KeyboardMatrix(left_joy))
    f.write(KeyboardMatrix(fire1_joy))
    f.write(KeyboardMatrix(up_joy))

    f.write(DecimalToBinary(len(name_software)))
    name_software_bin=bytearray(removeFrenchChars(name_software),'ascii')
    name_software_bin.append(0x00)
    f.write(name_software_bin)
    f.close()



def removeFrenchChars(mystr):

  
    mystr=mystr.replace(u'\xaa', "u")
    mystr=mystr.replace(u'\xa7', "c")
    mystr=mystr.replace(u'\xa0', u'a')
    mystr=mystr.replace(u'\xa2', u'a')
    mystr=mystr.replace(u'\xa8', u'e') # e tréma

    mystr=mystr.replace(u'\xbb', u'c') # ç
    mystr=mystr.replace(u'\xb9', u'u') # ù
    mystr=mystr.replace(u'\xb4', u'o') # ù

    mystr=mystr.replace(u'\xeb', u'e') # e tréma lower case
    mystr=mystr.replace(u'\xe8', u'e') # è
    
    mystr=mystr.replace("Ã¨", "e") # è pour mystère de Kikekankoi
    

    mystr=mystr.replace("Ã©", "e")
    mystr=mystr.replace("é", "e")

    mystr=mystr.replace("ê", "e")
    mystr=mystr.replace("ë", "e")
    mystr=mystr.replace("ç", "c")
    mystr=mystr.replace("°", " ")
    mystr=mystr.replace("Â", " ")


    mystr=mystr.replace("à", "a")
    mystr=mystr.replace("â", "a")

    mystr=mystr.replace("ô", "o")
    mystr=mystr.replace("ï", "i")
    mystr=mystr.replace("î", "i")
    mystr=mystr.replace("©", "")
    mystr=mystr.replace("Ã", "e")

    
    
    
    
    return mystr

def fileToExecuteTruncateTo8Letters(filename):
  
    head, tail = os.path.split(filename)
    filenametap=tail.lower().replace(" ", "").replace("-", "").replace("_", "")
    print("Filenametap : "+filenametap)
    tcnf=filenametap.split('.')
    filenametapext=tcnf[1]
    filenametapbase=tcnf[0]
    filenametap8bytesLength=filenametapbase[0:8]+"."+filenametapext
    
    return filenametap8bytesLength.upper()


def buildMdFile(filenametap8bytesLength,dest,letter,name_software,date_software,download_platform_software,programmer_software,junk_software):
    md_software="# "+removeFrenchChars(name_software)+"\n"
    #md_software=md_software+"Type : "+download_platform_software+"\n"
    tdate_software=date_software.split('-')
    year=tdate_software[0]
    md_software=md_software+"Release Date : "+year+"\n"
    md_software=md_software+"Platform : "
    match = re.search('A', download_platform_software)
    doslash="no"
    if match:
        md_software=md_software+"Atmos"
        doslash="yes"
    match = re.search('O', download_platform_software)
    if match:
        if doslash=="yes":
            md_software=md_software+"/"
        md_software=md_software+"Oric-1"
        doslash="no"                

    md_software=md_software+"\n"
            
    md_software=md_software+"Programmer : "+removeFrenchChars(programmer_software)+"\n"
    #md_software=md_software+"Origin : "+programmer_software+"\n"
    md_software=md_software+"Informations : "+removeFrenchChars(junk_software)+"\n"
            
    #print(md_software)
            
    md=filenametap8bytesLength+".md"
    file_md_path=dest+"/"+letter+"/"+md
    f = open(file_md_path, "wb")
    md_software = re.sub(u"\u2013", "-", md_software)
    md_software = re.sub(u"\u2019", "'", md_software)
    
    #md_software = md_software.decode('utf-8')
    #md_software = md_software.replace("\u2013", "-") #en dash
    md_bin=bytearray(md_software,'ascii')
    f.write(md_bin)
    f.close()

def BuildDsk(platform_software,letter,destpath,destetc,name_software,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy):
    CreateTargetFolder(destpath,destetc,letter)
    print("[DSK]Copying dsk : "+tmpfolderRetrieveSoftware+tail+" into :"+destpath+"/"+letter+"/"+filenametap8bytesLength+".dsk" )
    copyfile(tmpfolderRetrieveSoftware+tail,destpath+"/"+letter+"/"+filenametap8bytesLength+".dsk" )
    if not os.path.exists(destetc+"/"+letter):
        os.mkdir(destetc+"/"+letter)
    buildMdFile(filenametap8bytesLength,destpath,letter,name_software,date_software,platform_software,programmer_software,junk_software)
    buildDbFileSoftwareSingle(destetc,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)

def BuildTape(tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength,filenametapext,destroot,destetc,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy):
    #Hobbit ROM we copy also the tape file at the root of the sdcard
    print("Copying tape : "+tmpfolderRetrieveSoftware+tail+" to : "+dest+"/"+letter+"/"+filenametap8bytesLength+"."+filenametapext)
    print("Rom basic id : "+str(rombasic11))
    CreateTargetFolder(dest,destetc,letter)
    copyfile(tmpfolderRetrieveSoftware+tail,dest+"/"+letter+"/"+filenametap8bytesLength+"."+filenametapext)

#$trom["0"]="undefined";
#$trom["4"]="Rom Hobbit";
#$trom["1"]="Rom jeux atmos";
#$trom["2"]="Rom atmos normale";
#$trom["3"]="Rom Oric-1";
##$trom["99"]="NOK: no working ROM";
#$trom["253"]="NOK : Does not load";
#$trom["254"]="NOK : game ROM error: file not found";
#$trom["255"]="NOK : Game ROM altered charset";


    # Rom hobbit 
    if rombasic11=="4":
        print("Copy : "+tmpfolderRetrieveSoftware+tail+" to : "+destroot+"/"+filenametap8bytesLength+"."+filenametapext )
        copyfile(tmpfolderRetrieveSoftware+tail,destroot+"/"+filenametap8bytesLength+"."+filenametapext )
        # Force to ROM 0 : hobbit ROM
        rombasic11=0
    # In oric.org we have roms id to declare if a game is working or not, and if it's 
    if rombasic11!="0" and rombasic11!="1" and rombasic11!="2":    
        rombasic11=1

    if not os.path.exists(destetc+"/"+letter):
        os.mkdir(destetc+"/"+letter)
    print("Writing in db file rom id : ",str(rombasic11))
    buildMdFile(filenametap8bytesLength,dest,letter,name_software,date_software,download_platform_software,programmer_software,junk_software)
    buildDbFileSoftwareSingle(destetc,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)

def CheckTape(filename,tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength,filenametapext,destroot,destetc,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy):
    if filename=="":
        return 1


    if extension=="tap":
        print("Found tape file : "+removeFrenchChars(name_software))
        

        BuildTape(tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength,filenametapext,destroot,destetc,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
        # main db
        
        return 0
    return 1


def  BuildRom(download_label,name_software,cnf,download_file,tmpfolderRetrieveSoftware,destpath,letter,filenametap8bytesLength):
    # remove rom in the name
    name_software=name_software.replace(" ROMS","")
    name_software=name_software.replace(" ROM","")
    
    cnf=cnf+"["+name_software+" ("+download_label+")"+"]"
    cnf=cnf+"\n"
    cnf=cnf+"path=/usr/share/roms/"+letter+"/"+filenametap8bytesLength+".rom"+"\n"
    print("[ROM] Copying ROM : "+tmpfolderRetrieveSoftware+tail+" into :"+destpath+"/"+letter+"/"+filenametap8bytesLength+".rom" )
    copyfile(tmpfolderRetrieveSoftware+tail,destpath+"/"+letter+"/"+filenametap8bytesLength+"rom")
    
    return cnf

def RuleLoader(flags_software):
           # rules for software in the launcher ?
            # Does the first download is an atmos mode ? 
            # Yes we place it

            # Definition of FLAGS
            # A : Atmos and tape file
            # O : Oric-1 and tape file
    print("Flags ruleLoader : "+ flags_software)
    flag=""
    # Priority : Atmos
    if (flags_software.find('A') != -1 and flags_software.find('K') != -1):
        return 'A'

    if (flags_software.find('O') != -1 and flags_software.find('K') != -1):
        return 'O'

    return flag


def isOric1(flags_software):
           # rules for software in the launcher ?
            # Does the first download is an atmos mode ? 
            # Yes we place it

            # Definition of FLAGS
            # A : Atmos and tape file
            # O : Oric-1 and tape file
    print("Flags ruleLoader : "+ flags_software)
    flag=""
    if (flags_software.find('O') != -1 and flags_software.find('K') != -1):
        flag='O'
        
        return flag
    return flag


def isAtmos(flags_software):
           # rules for software in the launcher ?
            # Does the first download is an atmos mode ? 
            # Yes we place it

            # Definition of FLAGS
            # A : Atmos and tape file
            # O : Oric-1 and tape file
    print("Flags ruleLoader : "+ flags_software)
    flag=""
    if (flags_software.find('A') != -1 and flags_software.find('K') != -1):
        flag='A'
        
        return flag
    return flag

def isRom(flags_software):
           # rules for software in the launcher ?
            # Does the first download is an atmos mode ? 
            # Yes we place it

            # Definition of FLAGS
            # A : Atmos and tape file
            # O : Oric-1 and tape file
    
    flag=""
    if (flags_software.find('R') != -1):
        flag='R'
        print("Is ROM : "+ flags_software)
        
        return flag
    return flag


def RetriveSoftwareInTmpFolder(pathFileToDownload,tmpfolderRetrieveSoftware):
        b_obj_tape = BytesIO() 
        crl_tape = pycurl.Curl() 

        # Set URL value
        crl_tape.setopt(crl_tape.URL, 'https://cdn.oric.org/games/software/'+pathFileToDownload)
        crl_tape.setopt(crl_tape.SSL_VERIFYHOST, 0)
        crl_tape.setopt(crl_tape.SSL_VERIFYPEER, 0)
        # Write bytes that are utf-8 encoded
        crl_tape.setopt(crl_tape.WRITEDATA, b_obj_tape)

        # Perform a file transfer 
        crl_tape.perform() 

        # End curl session
        crl_tape.close()

        # Get the content stored in the BytesIO object (in byte characters) 
        get_body_tape = b_obj_tape.getvalue()

        # Decode the bytes stored in get_body to HTML and print the result 
        #print('Output of GET request:\n%s' % get_body.decode('utf8')) 




        head, tail = os.path.split(pathFileToDownload)

        f = open(tmpfolderRetrieveSoftware+"/"+tail, "wb")
        f.write(get_body_tape)
        f.close()

def CheckZip(filename):
    extension=download_1_file[-3:].lower()
    if extension=="zip":
        
        return 0
    return 1

def CheckDsk(download_platform_software,letter,destftdos,destetcftdos,name_software,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy):
    extension=download_platform_software[-3:].lower()
    if extension=="dsk":
        match = re.search('J', download_platform_software)
        print("[DSK] download_platform_software : "+download_platform_software)
        if match:
            # Jasmin
            print ('[DSK] jasmin/ftdos dsk file')
            BuildDsk(download_platform_software,letter,destftdos,destetcftdos,name_software,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
            return 0

        match = re.search('S', download_platform_software)
        if match:
            # Sedoric
            print ('[DSK] Sedoric dsk file')
            BuildDsk(download_platform_software,letter,destsedoric,destetcsedoric,name_software,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
            return 0
    return 1

def DecimalToBinary(num):
    return int(num).to_bytes(1, byteorder='little')

def DecimalTo16bits(num):
    return int(num).to_bytes(2, byteorder='little')

def CreateTargetFolder(dest,destetc,letter):
    folder=dest+'/'+letter
    folderdb=destetc+'/'+letter
    #print(folder)
    directory = os.path.dirname(folder)
    if not os.path.exists(folder) and folder!="":
        print("######################## Create "+folder)
        os.mkdir(folder)
        
    if not os.path.exists(folderdb) and folderdb!="" and destetc!="":
        # destroms,"",letter)
        print("######################## Create "+folderdb)
        os.mkdir(folderdb)
        

def KeyboardMatrix(num):
    keyboardMatrixTab=[
           #                                        LeftRight
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,172 ,188 , #0..9
           #          RET 
            180 ,156 ,175 ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #10..19
           #                                   ESC 
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,169 ,0   ,0   , #20..29
           #          ESP
            0   ,0   ,132 ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #30..39
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #40..49
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   , #50..59
           #                         A    B    C    D    E
            140 ,0   ,148   ,0   ,0   ,174 ,146 ,186 ,185 ,158  , #60..69
           #F    G    H    I    J    K    L    M    N    O
            153 ,150 ,142 ,141 ,129 ,131 ,143 ,130 ,136 ,149  , #70..79
           #P    Q    R    S     T    U    V    W    X    Y 
            157 ,177 ,145 ,182 ,137 ,133 ,152 ,180 ,176 ,134 , #80..89
           #Z 
            170 ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    , #90..99

            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #100..109
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #110..119
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #120..129
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #130..139
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #140..149
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #150..159
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #160..169
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #170..179
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #180..189
            0   ,0   ,0   ,0   ,0   ,0   ,0   ,0  ,0  , 0  , #190..199


            ] 
    key=keyboardMatrixTab[int(num)]
    return DecimalToBinary(key)

def manage_download(download_file,download_platform,download_label,tmpfolderRetrieveSoftware,name_software,id_software,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy,category_software,id_download):
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
    global nb_of_games
    global utils_db_str
    global nb_of_tools
    global demos_db_str
    global nb_of_demo
    global unsorted_db_str
    global nb_of_unsorted
    global music_db_str
    global nb_of_music
    global basic10_main_db_str
    global basic11_main_db_str
    global skipping_list_error
    global download_1_high_priority
    global download_2_high_priority
    global download_3_high_priority
    global download_4_high_priority
    global download_5_high_priority
    global download_6_high_priority
    global download_7_high_priority


    if download_file!="":
        RetriveSoftwareInTmpFolder(download_file,tmpfolderRetrieveSoftware)
        extension=download_file[-3:].lower()
        head, tail = os.path.split(download_file)
        letter=tail[0:1].lower()

        CreateTargetFolder(dest,destetc,letter)
        print("###########################################################################################")
        print("[DOWNLOAD_"+str(id_download)+"] Generating : "+name_software+"/"+id_software)
        filenametap=tail.lower().replace(" ", "").replace("-", "").replace("_", "")
        tcnf=filenametap.split('.')
        filenametapext=tcnf[1]
        cnf=tcnf[0]+".db"
        filenametapbase=tcnf[0]
        filenametap8bytesLength=filenametapbase[0:8]
        filename8plus3=fileToExecuteTruncateTo8Letters(filenametap)
        skipping_list_error_txt=""
        print("[DOWNLOAD_"+str(id_download)+"] Filename : "+filenametap+" tail : "+tail+"  file : "+download_file)
        if isOric1(download_platform):
            CreateTargetFolder(dest_basic10,destetc_basic10,letter)
        
        if isRom(download_platform):
            if filenametapext=="rom":
                CreateTargetFolder(destroms,"",letter)
                roms_banks_cnf=BuildRom(download_label,name_software,roms_banks_cnf,download_file,tmpfolderRetrieveSoftware,destroms,letter,filenametap8bytesLength)
                nb_of_roms=nb_of_roms+1
            else:
                print("[ROM][DOWNLOAD_"+str(id_download)+"] is not a .rom extension")
            return ""

        if CheckZip(download_file)==0:
            flag=""
            flag=RuleLoader(download_platform)
            if (flag!=""):
                skipping_list_error_txt="[ZIP][DOWNLOAD_"+str(id_download)+"] Skipping download (reason : ZIP) : "+removeFrenchChars(name_software)+"/Flags : "+download_1_platform+" "+id_software+"\n"
                print("[ZIP][DOWNLOAD_"+str(id_download)+"] seems to be a tape file but it's zipped")
            print("[ZIP][DOWNLOAD_"+str(id_download)+"] zip (Skipping) id_software :"+id_software)
            return ""

        if CheckDsk(download_file,letter,destftdos,destetcftdos,name_software,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)==0:    
            print("[DSK][DOWNLOAD_"+str(id_download)+"] Id_software:"+id_software)
            return ""

        matchRule=0
        flag=""
        if CheckTape(download_file,tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength,filenametapext,destroot,destetc,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)==0:
            
            print("[TAPE][DOWNLOAD_"+str(id_download)+"] Check tape download")
            addSoftware=filenametap8bytesLength.upper()+';'+removeFrenchChars(name_software)+'\0'
            if isOric1(download_platform):
                basic10_main_db_str=basic10_main_db_str+addSoftware
                BuildTape(tmpfolderRetrieveSoftware,tail,dest_basic10,letter,filenametap8bytesLength,filenametapext,destroot,destetc_basic10,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
                print("[TAPE][DOWNLOAD_"+str(id_download)+"][BASIC10] Adding "+filenametap8bytesLength+" to basic10 command")
                number_of_software_basic10=number_of_software_basic10+1
                #buildDbFileSoftwareSingle(destetc_basic10,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
            if isAtmos(download_platform):
                basic_main_db_str=basic_main_db_str+addSoftware
                print("[TAPE][DOWNLOAD_"+str(id_download)+"][BASIC11] Adding "+filenametap8bytesLength+" to basic11 command")
                number_of_software_basic11=number_of_software_basic11+1

            lenAddSoftware+=len(addSoftware)
            main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
            flag=RuleLoader(download_platform)
            if (download_1_high_priority==1):
                addSoftwareLauncher=fileToExecuteTruncateTo8Letters(download_file)+';'+removeFrenchChars(name_software)+';'+flag+';\0'
                matchRule=1
                print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Inserting download "+str(id_download)+" for ("+removeFrenchChars(name_software)+") with flags : "+flag)
                if category_software=="1" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category game in loader db")
                    game_db_str=game_db_str+addSoftwareLauncher
                    nb_of_games=nb_of_games+1
                if category_software=="2" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category util in loader db")
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1                
                #Tape ins game
                if category_software=="3" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category game in loader db")
                    game_db_str=game_db_str+addSoftwareLauncher
                    nb_of_games=nb_of_games+1                
                # Tape ins utility
                if category_software=="4" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category util in loader db")
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1
                # Tape ins unknow category set to utils
                if category_software=="5" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category util in loader db")
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1                
                if category_software=="6" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category dem in loader db")
                    demos_db_str=demos_db_str+addSoftwareLauncher          
                    nb_of_demo=nb_of_demo+1
                if category_software=="7" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category unsorted in loader db")
                    unsorted_db_str=unsorted_db_str+addSoftwareLauncher
                    nb_of_unsorted=nb_of_unsorted+1
                # Game from book
                if category_software=="8" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category games in loader db")
                    game_db_str=game_db_str+addSoftwareLauncher
                    nb_of_games=nb_of_games+1
                # Tape ins book utility
                if category_software=="9" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category utils in loader db")
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1                
                if category_software=="10" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_"+str(id_download)+"][LOADER] Add in category music in loader db")
                    music_db_str=music_db_str+addSoftwareLauncher
                    nb_of_music=nb_of_music+1
            #else:
            #    print("[TAPE][DOWNLOAD_1] Skipping first download trying second download : "+removeFrenchChars(name_software))
            #    skipping_list_error=skipping_list_error+"Skipping first download : "+removeFrenchChars(name_software)+"/Flags : "+download_platform+" "+id_software+"\n"

        




exist_ok=True
if not os.path.exists(dest):
    pathlib.Path(dest).mkdir(parents=True)
if not os.path.exists(destetc):
    pathlib.Path(destetc).mkdir(parents=True)    

# Basic10 path
if not os.path.exists(dest_basic10):
    pathlib.Path(dest_basic10).mkdir(parents=True)
if not os.path.exists(destetc_basic10):
    pathlib.Path(destetc_basic10).mkdir(parents=True)    

# Roms path
if not os.path.exists(destroms):
    pathlib.Path(destroms).mkdir(parents=True)
if not os.path.exists(destetc_roms):
    pathlib.Path(destetc_roms).mkdir(parents=True)    


# Launcher
if not os.path.exists(destlauncher):
    pathlib.Path(destlauncher).mkdir(parents=True)        



# ftdos    
if not os.path.exists(destftdos):
    pathlib.Path(destftdos).mkdir(parents=True)
if not os.path.exists(destetcftdos):
    pathlib.Path(destetcftdos).mkdir(parents=True)    

#skipping_problem_tape_filename

# sedoric
if not os.path.exists(destsedoric):
    pathlib.Path(destsedoric).mkdir(parents=True)
if not os.path.exists(destetcsedoric):
    pathlib.Path(destetcsedoric).mkdir(parents=True)        

if not os.path.exists(tmpfolderRetrieveSoftware):
    pathlib.Path(tmpfolderRetrieveSoftware).mkdir(parents=True)    

print(computeVersion())

print("Retrieve json file from oric.org ...")
b_obj = BytesIO() 
crl = pycurl.Curl() 

# Set URL value
crl.setopt(crl.URL, 'http://api.oric.org/0.2/softwares/?sorts=name_software')
#crl.setopt(crl.URL, 'http://api.oric.org/0.2/softwares/125')

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


basic_main_db_str=""
basic10_main_db_str=""
game_db_str=""
music_db_str=""
demos_db_str=""
utils_db_str=""
unsorted_db_str=""

skipping_list_error=""
#                       low, high
main_db_table_software=[1,0]
lenAddSoftware=0



for i in range(len(datastore)):
    
    #Use the new datastore datastructure
    id_software=datastore[i]["id"]
    tapefile=datastore[i]["download_software"]

    name_software=datastore[i]["name_software"]
    programmer_software=datastore[i]["programmer_software"]
    download_platform_software=datastore[i]["download_platform_software"]
    
    download_1_platform=datastore[i]["platform_software"]
    download_2_platform=datastore[i]["second_download_platform_software"]
    download_3_platform=datastore[i]["download_3_platform"]
    download_4_platform=datastore[i]["download_4_platform"]
    download_5_platform=datastore[i]["download_5_platform"]
    download_6_platform=datastore[i]["download_6_platform"]    
    download_7_platform=datastore[i]["download_7_platform"]
    
    download_1_file=datastore[i]["download_software"]
    download_2_file=datastore[i]["second_download_software"]
    download_3_file=datastore[i]["download_3_path"]
    download_4_file=datastore[i]["download_4_path"]
    download_5_file=datastore[i]["download_5_path"]
    download_6_file=datastore[i]["download_6_path"]
    download_7_file=datastore[i]["download_7_path"]
    
    download_1_label=datastore[i]["download_1_label"]
    download_2_label=datastore[i]["download_2_label"]
    download_3_label=datastore[i]["download_3_label"]
    download_4_label=datastore[i]["download_4_label"]
    download_5_label=datastore[i]["download_5_label"]
    download_6_label=datastore[i]["download_6_label"]
    download_7_label=datastore[i]["download_7_label"]    

    category_software=datastore[i]["category_software"]
    junk_software=datastore[i]["junk_software"]
    date_software=datastore[i]["date_software"]
    name_software=name_software.replace("é", "e")
    name_software=name_software.replace("è", "e")
    name_software=name_software.replace("ç", "c")
    name_software=name_software.replace("°", " ")
    name_software=name_software.replace("à", "a")
    name_software=name_software.replace("â", "o")
    joystick_management_state=datastore[i]["joystick_management_state"]
    junk_software=removeFrenchChars(junk_software)

    

    programmer_software=programmer_software.replace("é", "e")
    programmer_software=programmer_software.replace("è", "e")
    programmer_software=programmer_software.replace("ç", "c")
    programmer_software=programmer_software.replace("°", " ")
    programmer_software=programmer_software.replace("à", "a")
    programmer_software=programmer_software.replace("ô", "o")


    rombasic11=datastore[i]["basic11_ROM_TWILIGHTE"]
    up_joy=datastore[i]["up_joy"]
    down_joy=datastore[i]["down_joy"]
    right_joy=datastore[i]["right_joy"]
    left_joy=datastore[i]["left_joy"]
    fire1_joy=datastore[i]["fire1_joy"]
    fire2_joy=datastore[i]["fire2_joy"]
    fire3_joy=0
    #print(datastore[i])
    #print(tapefile)
    if download_1_file!="":
        RetriveSoftwareInTmpFolder(download_1_file,tmpfolderRetrieveSoftware)
        extension=download_1_file[-3:].lower()
        head, tail = os.path.split(download_1_file)
        letter=tail[0:1].lower()

        CreateTargetFolder(dest,destetc,letter)
       


            
        
        print("###########################################################################################")
        print("Generating : "+name_software+"/"+id_software)
        filenametap=tail.lower().replace(" ", "").replace("-", "").replace("_", "")
        tcnf=filenametap.split('.')
        filenametapext=tcnf[1]
        cnf=tcnf[0]+".db"
        filenametapbase=tcnf[0]
        filenametap8bytesLength=filenametapbase[0:8]
        filename8plus3=fileToExecuteTruncateTo8Letters(filenametap)
        
        print("Filenametap : "+filenametap+" tail : "+tail+" tape file : "+tapefile)

        if isOric1(download_1_platform):
            CreateTargetFolder(dest_basic10,destetc_basic10,letter)

        if isRom(download_1_platform):
            if filenametapext=="rom":
                CreateTargetFolder(destroms,"",letter)
                roms_banks_cnf=BuildRom(download_1_label,name_software,roms_banks_cnf,download_1_file,tmpfolderRetrieveSoftware,destroms,letter,filenametap8bytesLength)
                nb_of_roms=nb_of_roms+1
            else:
                print("[ROM] is not a .rom extension")
        


        if CheckZip(download_1_file)==0:
            flag=""
            flag=RuleLoader(download_1_platform)
            if (flag!=""):
                skipping_list_error=skipping_list_error+"Skipping download (reason : ZIP) : "+removeFrenchChars(name_software)+"/Flags : "+download_1_platform+" "+id_software+"\n"
                print("[ZIP] seems to be a tape file but it's zipped")
            print("[ZIP] zip (Skipping) id_software :"+id_software)

        if CheckDsk(download_1_file,letter,destftdos,destetcftdos,name_software,filenametap8bytesLength,tail,tmpfolderRetrieveSoftware,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)==0:    
            print("[DSK] Id_software:"+id_software)
        matchRule=0
        flag=""
        # Download 1

        # Manage priority : 
        # Atmos + tape if available is inserted (high priority)
        # Oric-1 + tape lower priority than atmos
        download_1_high_priority=0
        download_2_high_priority=0
        download_3_high_priority=0
        download_4_high_priority=0
        
        if (download_1_platform.find('A') != -1 and download_1_platform.find('K') != -1):
            download_1_high_priority=1
        else:
            if (download_2_platform.find('A') != -1 and download_2_platform.find('K') != -1):
                download_2_high_priority=1
            else:
                # Oric-1
                if (download_1_platform.find('O') != -1 and download_1_platform.find('K') != -1):
                    download_1_high_priority=1
                else:
                    if (download_2_platform.find('O') != -1 and download_2_platform.find('K') != -1):
                        download_2_high_priority=1





        if CheckTape(download_1_file,tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength,filenametapext,destroot,destetc,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)==0:
            
            print("[TAPE][DOWNLOAD_1] Check tape download 1")
            addSoftware=filenametap8bytesLength.upper()+';'+removeFrenchChars(name_software)+'\0'
            if isOric1(download_1_platform):
                basic10_main_db_str=basic10_main_db_str+addSoftware
                BuildTape(tmpfolderRetrieveSoftware,tail,dest_basic10,letter,filenametap8bytesLength,filenametapext,destroot,destetc_basic10,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
                print("[TAPE][DOWNLOAD_1][ORIC1] Adding "+filenametap8bytesLength+" to basic10 command")
                number_of_software_basic10=number_of_software_basic10+1
                #buildDbFileSoftwareSingle(destetc_basic10,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
            if isAtmos(download_1_platform):
                basic_main_db_str=basic_main_db_str+addSoftware
                print("[TAPE][DOWNLOAD_1][ATMOS] Adding "+filenametap8bytesLength+" to basic11 command")
                number_of_software_basic11=number_of_software_basic11+1

            lenAddSoftware+=len(addSoftware)
            main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
            flag=RuleLoader(download_1_platform)
            if (download_1_high_priority==1):
                addSoftwareLauncher=fileToExecuteTruncateTo8Letters(download_1_file)+';'+removeFrenchChars(name_software)+';'+flag+';\0'
                matchRule=1
                print("[TAPE][DOWNLOAD_1] Inserting download 1 for ("+removeFrenchChars(name_software)+") with flags : "+flag)
                if category_software=="1" and addSoftwareLauncher!="":
                    game_db_str=game_db_str+addSoftwareLauncher
                    nb_of_games=nb_of_games+1
                if category_software=="2" and addSoftwareLauncher!="":
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1                
                #Tape ins game
                if category_software=="3" and addSoftwareLauncher!="":
                    game_db_str=game_db_str+addSoftwareLauncher
                    nb_of_games=nb_of_games+1                
                # Tape ins utility
                if category_software=="4" and addSoftwareLauncher!="":
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1
                # Tape ins unknow category set to utils
                if category_software=="5" and addSoftwareLauncher!="":
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1                
                if category_software=="6" and addSoftwareLauncher!="":
                    demos_db_str=demos_db_str+addSoftwareLauncher          
                    nb_of_demo=nb_of_demo+1
                if category_software=="7" and addSoftwareLauncher!="":
                    unsorted_db_str=unsorted_db_str+addSoftwareLauncher
                    nb_of_unsorted=nb_of_unsorted+1
                # Game from book
                if category_software=="8" and addSoftwareLauncher!="":
                    game_db_str=game_db_str+addSoftwareLauncher
                    nb_of_games=nb_of_games+1
                # Tape ins book utility
                if category_software=="9" and addSoftwareLauncher!="":
                    utils_db_str=utils_db_str+addSoftwareLauncher
                    nb_of_tools=nb_of_tools+1                
                if category_software=="10" and addSoftwareLauncher!="":
                    print("[TAPE][DOWNLOAD_1] Add in category music in loader db")
                    music_db_str=music_db_str+addSoftwareLauncher
                    nb_of_music=nb_of_music+1
            else:
                print("[TAPE][DOWNLOAD_1] Skipping first download trying second download : "+removeFrenchChars(name_software))
                skipping_list_error=skipping_list_error+"Skipping first download : "+removeFrenchChars(name_software)+"/Flags : "+download_1_platform+" "+id_software+"\n"


        if download_2_file!="":
            extension=download_2_file[-3:].lower()
            head, tail = os.path.split(download_2_file)
            letter=tail[0:1].lower()
            filenametap=tail.lower().replace(" ", "").replace("-", "").replace("_", "")
            tcnf=filenametap.split('.')           
            filenametapext=tcnf[1]
            filenametapbase=tcnf[0]
            filenametap8bytesLength=filenametapbase[0:8]
            RetriveSoftwareInTmpFolder(download_2_file,tmpfolderRetrieveSoftware)

            if isRom(download_2_platform):
                if filenametapext=="rom":
                    CreateTargetFolder(destroms,"",letter)
                    roms_banks_cnf=BuildRom(download_2_label,name_software,roms_banks_cnf,download_2_file,tmpfolderRetrieveSoftware,destroms,letter,filenametap8bytesLength)
                    nb_of_roms=nb_of_roms+1
                else:
                    print("[ROM][DOWNLOAD2] is not a .rom extension")
            
            
            if flag=="" and CheckTape(download_2_file,tmpfolderRetrieveSoftware,tail,dest,letter,filenametap8bytesLength,filenametapext,destroot,destetc,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)==0:
                

                addSoftware=filenametap8bytesLength.upper()+';'+removeFrenchChars(name_software)+'\0'
                if isOric1(download_2_platform):
                    basic10_main_db_str=basic10_main_db_str+addSoftware
                    BuildTape(tmpfolderRetrieveSoftware,tail,dest_basic10,letter,filenametap8bytesLength,filenametapext,destroot,destetc_basic10,name_software,date_software,download_platform_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
                    print("[TAPE][DOWNLOAD_2][ORIC1] Adding (download2) "+filenametap8bytesLength+" to basic10 command")
                    number_of_software_basic10=number_of_software_basic10+1
                    #buildDbFileSoftwareSingle(destetc_basic10,letter,name_software,filenametap8bytesLength,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy)
                if isAtmos(download_2_platform):
                    basic_main_db_str=basic_main_db_str+addSoftware
                    print("[TAPE][DOWNLOAD_2][ATMOS] Adding (download2)"+filenametap8bytesLength+"to basic11 command")
                    number_of_software_basic11=number_of_software_basic11+1

                lenAddSoftware+=len(addSoftware)
                main_db_table_software.append(lenAddSoftware.to_bytes(2, 'little'))
                flag=RuleLoader(download_2_platform)
                if (download_2_high_priority==1):
                    print("[TAPE][DOWNLOAD_2] Inserting download 2 in loader db for ("+removeFrenchChars(name_software)+") with flag : "+flag)
                    addSoftwareLauncher=fileToExecuteTruncateTo8Letters(download_2_file)+';'+removeFrenchChars(name_software)+';'+flag+';\0'
                    matchRule=1
                    if category_software=="1" and addSoftwareLauncher!="":
                        game_db_str=game_db_str+addSoftwareLauncher
                        nb_of_games=nb_of_games+1
                    if category_software=="2" and addSoftwareLauncher!="":
                        utils_db_str=utils_db_str+addSoftwareLauncher
                        nb_of_tools=nb_of_tools+1                
                    #Tape ins game
                    if category_software=="3" and addSoftwareLauncher!="":
                        game_db_str=game_db_str+addSoftwareLauncher
                        nb_of_games=nb_of_games+1                
                    # Tape ins utility
                    if category_software=="4" and addSoftwareLauncher!="":
                        utils_db_str=utils_db_str+addSoftwareLauncher
                        nb_of_tools=nb_of_tools+1
                    # Tape ins unknow category set to utils
                    if category_software=="5" and addSoftwareLauncher!="":
                        utils_db_str=utils_db_str+addSoftwareLauncher
                        nb_of_tools=nb_of_tools+1                
                    if category_software=="6" and addSoftwareLauncher!="":
                        demos_db_str=demos_db_str+addSoftwareLauncher          
                        nb_of_demo=nb_of_demo+1
                    if category_software=="7" and addSoftwareLauncher!="":
                        unsorted_db_str=unsorted_db_str+addSoftwareLauncher
                        nb_of_unsorted=nb_of_unsorted+1
                    # Game from book
                    if category_software=="8" and addSoftwareLauncher!="":
                        game_db_str=game_db_str+addSoftwareLauncher
                        nb_of_games=nb_of_games+1
                    # Tape ins book utility
                    if category_software=="9" and addSoftwareLauncher!="":
                        utils_db_str=utils_db_str+addSoftwareLauncher
                        nb_of_tools=nb_of_tools+1                
                    if category_software=="10" and addSoftwareLauncher!="":
                        print("########### Add music")
                        music_db_str=music_db_str+addSoftwareLauncher
                        nb_of_music=nb_of_music+1
                else:
                    print("Skipping second download, not .tap file found : "+removeFrenchChars(name_software))
                    skipping_list_error=skipping_list_error+"Skipping second download : "+removeFrenchChars(name_software)+"/Flags : "+download_2_platform+" "+id_software+"\n"

                if download_1_high_priority==0 and download_2_high_priority==0:
                    print("!!!Error!!! No compatible support found for : "+removeFrenchChars(name_software))

        manage_download(download_3_file,download_3_platform,download_3_label,tmpfolderRetrieveSoftware,name_software,id_software,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy,category_software,3)
        manage_download(download_4_file,download_4_platform,download_4_label,tmpfolderRetrieveSoftware,name_software,id_software,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy,category_software,4)
        manage_download(download_5_file,download_5_platform,download_5_label,tmpfolderRetrieveSoftware,name_software,id_software,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy,category_software,5)
        manage_download(download_6_file,download_6_platform,download_6_label,tmpfolderRetrieveSoftware,name_software,id_software,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy,category_software,6)
        manage_download(download_7_file,download_7_platform,download_7_label,tmpfolderRetrieveSoftware,name_software,id_software,date_software,programmer_software,junk_software,version_bin,rombasic11,fire2_joy,fire3_joy,down_joy,right_joy,left_joy,fire1_joy,up_joy,category_software,7)
EOF=0xFF
print("Write basic11 db"+str(number_of_software_basic11))
f = open(destetc+"/"+basic_main_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic_main_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic10 db/nb : "+str(number_of_software_basic10))
f = open(destetc_basic10+"/"+basic10_main_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic10_main_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()


#print(main_db_table_software)
# indexed
f = open(destetc+"/"+basic_main_db_indexed, "wb")
f.write(DecimalToBinary(version_bin))
f.write(bytearray(basic_main_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

# V0 loader

print("Write basic_games_db/nb : "+str(nb_of_games))
f = open(destlauncher+"/"+basic_games_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_games))
f.write(bytearray(game_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()



print("Write basic_demos_db/nb : "+str(nb_of_demo))
f = open(destlauncher+"/"+basic_demos_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_demo))
f.write(bytearray(demos_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_utils_db/nb : "+str(nb_of_tools))
f = open(destlauncher+"/"+basic_utils_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_tools))
f.write(bytearray(utils_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_unsorted_db")
f = open(destlauncher+"/"+basic_unsorted_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_unsorted))
f.write(bytearray(unsorted_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_music_db/nb : "+str(nb_of_music))
f = open(destlauncher+"/"+basic_music_db, "wb")
f.write(DecimalToBinary(version_bin))
f.write(DecimalTo16bits(nb_of_music))
f.write(bytearray(music_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write roms/nb : "+str(nb_of_roms))
f = open(destetc_roms+"/bankstmp.cnf", "wb")
f.write(bytearray(roms_banks_cnf,'ascii'))
f.close()


# V1 loader

print("Write basic_games_db V2 /nb : "+str(nb_of_games))
f = open(destlauncher+"/"+basic_games_db_v2, "wb")
f.write(DecimalToBinary(version_bin_v2))
f.write(DecimalToBinary(number_of_db_part))
f.write(bytearray(computeVersion(),'ascii'))
f.write(DecimalTo16bits(nb_of_games))
f.write(bytearray(game_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()



print("Write basic_demos_db V2/nb : "+str(nb_of_demo))
f = open(destlauncher+"/"+basic_demos_db_v2, "wb")
f.write(DecimalToBinary(version_bin_v2))
f.write(DecimalToBinary(number_of_db_part))
f.write(bytearray(computeVersion(),'ascii'))
f.write(DecimalTo16bits(nb_of_demo))
f.write(bytearray(demos_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_utils_db V2/nb : "+str(nb_of_tools))
f = open(destlauncher+"/"+basic_utils_db_v2, "wb")
f.write(DecimalToBinary(version_bin_v2))
f.write(DecimalToBinary(number_of_db_part))
f.write(bytearray(computeVersion(),'ascii'))
f.write(DecimalTo16bits(nb_of_tools))
f.write(bytearray(utils_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_unsorted_db v2")
f = open(destlauncher+"/"+basic_unsorted_db_v2, "wb")
f.write(DecimalToBinary(version_bin_v2))
f.write(DecimalToBinary(number_of_db_part))
f.write(bytearray(computeVersion(),'ascii'))
f.write(DecimalTo16bits(nb_of_unsorted))
f.write(bytearray(unsorted_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

print("Write basic_music_db/nb v2: "+str(nb_of_music))
f = open(destlauncher+"/"+basic_music_db_v2, "wb")
f.write(DecimalToBinary(version_bin_v2))
f.write(DecimalToBinary(number_of_db_part))
f.write(bytearray(computeVersion(),'ascii'))
f.write(DecimalTo16bits(nb_of_music))
f.write(bytearray(music_db_str,'ascii'))
f.write(DecimalToBinary(EOF))
f.close()

#print("Write roms/nb V2 : "+str(nb_of_roms))
#f = open(destetc_roms+"/bankstmp.cnf", "wb")
#f.write(bytearray(roms_banks_cnf,'ascii'))
#f.close()



print("Write skipping_problem_tape_filename")
f = open(skipping_problem_tape_filename, "wb")
f.write(bytearray(skipping_list_error,'ascii'))
f.close()



#basic_utils_db="utils.db"
#basic_unsorted_db="unsorted.db"

