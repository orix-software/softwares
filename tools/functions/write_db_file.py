from datetime import date

version_bin_v2 = "1"
EOF=0xFF

def DecimalTo16bits(num):
    return int(num).to_bytes(2, byteorder='little')

def DecimalToBinary(num):
    return int(num).to_bytes(1, byteorder='little')

def computeVersion():
   # for m in range(1, 13):
    today = date.today()
    month = int(today.strftime("%m"))
    quarter = str(((month*3)//10)+1)

    strversion = today.strftime("%Y."+quarter+".%m.%d")
    return strversion

def write_db_file_v2(string_debug, nb_of_softwares, nb_of_parts, filenamedb, dbcontent):
    print(string_debug)
    f = open(filenamedb, "wb")
    f.write(DecimalToBinary(version_bin_v2))
    f.write(DecimalToBinary(nb_of_parts))
    f.write(bytearray(computeVersion(),'ascii'))
    f.write(DecimalTo16bits(nb_of_softwares))
    f.write(bytearray(dbcontent,'ascii'))
    f.write(DecimalToBinary(EOF))
    f.close()
