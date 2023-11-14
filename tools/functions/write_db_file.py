from datetime import date

version_bin_v2 = "1"
EOF=0xFF

def DecimalTo16bits(num):
    return int(num).to_bytes(2, byteorder='little')

def DecimalToBinary(num):
    return int(num).to_bytes(1, byteorder='little')


def KeyboardMatrix(num):
    keyboardMatrixTab = [
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

def computeVersion():
   # for m in range(1, 13):
    today = date.today()
    month = int(today.strftime("%m"))
    quarter = str(((month*3)//10)+1)

    strversion = today.strftime("%Y."+quarter+".%m.%d")
    return strversion

def write_db_file_v2(string_debug, nb_of_softwares, nb_of_parts, filenamedb, dbcontent):
    print(f"{ string_debug }/NB : { nb_of_softwares }")
    f = open(filenamedb, "wb")
    f.write(DecimalToBinary(version_bin_v2))
    f.write(DecimalToBinary(nb_of_parts))
    f.write(bytearray(computeVersion(),'ascii'))
    f.write(DecimalTo16bits(nb_of_softwares))
    f.write(bytearray(dbcontent,'ascii'))
    f.write(DecimalToBinary(EOF))
    f.close()

def populateDbFileWithTypeGame(addSoftwareLauncher, category_software, format_type):
    game_str = ""
    if category_software == "1" and addSoftwareLauncher != "":
        game_str = addSoftwareLauncher

    #Tape ins game
    if category_software == "3" and addSoftwareLauncher!="":
        game_str = addSoftwareLauncher

    if category_software=="8" and addSoftwareLauncher!="":
        game_str = addSoftwareLauncher

    if game_str == "":
        return game_str

    print(f"[ { format_type} ][DOWNLOAD][LOADER] Add in category games in loader db")
    return game_str

def populateDbFileWithTypeUtils(addSoftwareLauncher, category_software, format_type):

    utils_str = ""

    if category_software == "2" and addSoftwareLauncher != "":
        utils_str = addSoftwareLauncher

    if category_software == "4" and addSoftwareLauncher != "":
        utils_str = addSoftwareLauncher

    if category_software == "5" and addSoftwareLauncher != "":
        utils_str = addSoftwareLauncher

    if category_software == "9" and addSoftwareLauncher != "":
        utils_str = addSoftwareLauncher

    if utils_str == "":
        return utils_str

    print(f"[ { format_type} ][DOWNLOAD][LOADER] Add in category utils in loader db")
    return utils_str

def populateDbFileWithTypeDemo(addSoftwareLauncher, category_software, format_type):

    demos_str = ""

    if category_software == "6" and addSoftwareLauncher != "":
        demos_str = addSoftwareLauncher

    if demos_str == "":
        return demos_str

    print(f"[ { format_type} ][DOWNLOAD][LOADER] Add in category demos in loader db")
    return demos_str

def populateDbFileWithTypeMusic(addSoftwareLauncher, category_software, format_type):

    Music_str = ""

    if category_software == "10" and addSoftwareLauncher != "":
        Music_str = addSoftwareLauncher

    if Music_str == "":
        return Music_str

    print(f"[ { format_type} ][DOWNLOAD][LOADER] Add in category Music in loader db")
    return Music_str