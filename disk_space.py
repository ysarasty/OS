# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:30:24 2019

@author: DL5399
"""

from __future__ import print_function
import platform
import os
import socket
from prettytable import PrettyTable
import sys
import getpass
import psutil
import cx_Oracle


P_Version = sys.version[0]
Current_os = platform.system().lower()
hostname = socket.gethostname()
username = getpass.getuser()
line_awk = os.popen("which awk")
for line in line_awk:
    awk = line
awk = awk.replace('\n', ' ').replace('\r', '')
line_find = os.popen("which find")
for line in line_find:
    find = line
find = find.replace('\n', ' ').replace('\r', '')


def create_param_awk():
    file = os.popen("touch /tmp/params.awk")
    file = open("/tmp/params.awk", "w")
    file.write("BEGIN {gsub(\"[^[:digit:]]+\", \"\",$5)}")
    file.write("\n {print $6 \" \"$2\" \"$5}")
    file.close()


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def create_str(com):
    if com == 1:
        str_temp = ("df -Ph|" + awk + " --file /tmp/params.awk | sort -nrk 3 ")
    elif com == 2:
        if P_Version == "2":
            val2 = raw_input("\n Répertoire a vérifier: ")
        else:
            val2 = input("\n Répertoire a vérifier : ")
        val2 = val2.replace('\n', ' ').replace('\r', '')
        str_temp = (find + val2)
        str_temp = (str_temp + " -maxdepth 3 -type d -exec du -sh {} \\;|" + awk)
        str_temp = (str_temp + "'{print $2 \"  \" $1 }'| grep '[0-9]G\\>' |sort -nrk 2")
    elif com == 3:
        if P_Version == "2":
            print("Répertoire?")
            dir_target = raw_input("(Chemin complet) ")
        else:
            print("Dans quel répertoire?")
            dir_target = input("(Chemin complet)")
        dir_target = dir_target.replace('\n', ' ').replace('\r', '')
        str_temp = (find + " ")
        str_temp = (str_temp + dir_target)
        str_temp = (str_temp + " -type f -size +1G -exec du -sh {} \\;|sort -nrk 1")
    else:
        print("No way .....")
    return str_temp


def disk_partitions_space_status(all=False):
    retlist = []
    string_1 = create_str(1)
    f = os.popen(string_1)
    for line in f:
        if not all and line.startswith('Mounted'):
            continue
        fields = line.split()
        partition = fields[0]
        size_p = fields[1]
        if RepresentsInt(size_p):
            size_p = int(size_p)
        percentage = fields[2]
        if RepresentsInt(percentage):
            percentage = int(percentage)
        ntuple = (partition, size_p, percentage)
        retlist.append(ntuple)
    return retlist


def list_to_be_print(to_be_print, i):
    if i == 1:
        table_p = PrettyTable(['Filesystem', 'Size', 'Use%'])
        table_p.align["Filesystem"] = "l"
        table_p.align["Size"] = "r"
        table_p.align["Use%"] = "r"
    elif i == 2:
        table_p = PrettyTable(['Directory', 'Size'])
        table_p.align["Directory"] = "l"
        table_p.align["Size"] = "r"
    elif i == 3:
        table_p = PrettyTable(['File', 'Size'])
        table_p.align["File"] = "l"
        table_p.align["Size"] = "r"
    elif i == 4:
        table_p = PrettyTable(['Filesystem', 'Size', 'Use%'])
    elif i == 5:
        table_p = PrettyTable(['No', 'Tablespace'])
    for line in to_be_print:
        if not all:
            continue
        if i == 1:
            a = line[0]
            b = line[1]
            c = line[2]
            table_p.add_row([a, b, c])
        elif i == 2:
            a = line[0]
            b = line[1]
            table_p.add_row([a, b])
        elif i == 3:
            a = line[0]
            b = line[1]
            table_p.add_row([a, b])
    print(table_p)


def focus_file_system():
    print("\n\n")
    list_to_o = []
    i = 1
    create_param_awk()
    for part in disk_partitions_space_status():
        list_to_o.append(part)
    list_to_be_print(list_to_o, i)
    print("\n\n")
    return True


def directory_space_status():
    retlist = []
    string_t = create_str(2)
    print("\n Veuillez être patient \n")
#    print(string_t)
    f = os.popen(string_t)
    for line in f:
        fields = line.split()
        directory = fields[0]
        file_s = fields[1]
        if RepresentsInt(file_s):
            file_s = fields[2]
        ntuple = (directory, file_s)
        retlist.append(ntuple)
    return retlist


def file_space_status():
    retlist = []
    string_t = create_str(3)
    print("\n Veuillez être patient \n ")
#    print(string_t)
    f = os.popen(string_t)
    for line in f:
        fields = line.split()
        file_name = fields[1]
        file_s = fields[0]
        ntuple = (file_name, file_s)
        retlist.append(ntuple)
    return retlist


def focus_on_dir(aux):
    i = 2
    list_to_o = []
    if aux:
#        print(aux)
        for part in directory_space_status():
            list_to_o.append(part)
        list_to_be_print(list_to_o, i)
    if P_Version == "2":
        aux2 = int(raw_input("\n Aller plus profond? (Oui (1) | No (0) :"))
    else:
        aux2 = int(input("\n Aller plus profond? (Oui (1) | No (0) :"))
    if aux2 == 1:
        print("++++")
        focus_on_dir(True)
    elif aux2 == 0:
        print("----")
    else:
        print("\n SVP, Oui (1) | No (0)")
    return aux


def focus_on_file():
    list_to_o = []
    i = 3
    for part in file_space_status():
        list_to_o.append(part)
    list_to_be_print(list_to_o, i)


def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def query():
    q1 = ("select df.tablespace_name TB_name,")
    q1 = (q1 + " totalusedspace Used_MB,")
    q1 = (q1 + " (df.totalspace - tu.totalusedspace) Free_MB,")
    q1 = (q1 + " df.totalspace Total_MB,")
    q1 = (q1 + " round(100 * ( (df.totalspace - tu.totalusedspace)/ df.totalspace))")
    q1 = (q1 + " Pct_Free")
    q1 = (q1 + "  from ")
    q1 = (q1 + " (select tablespace_name,")
    q1 = (q1 + " round(sum(bytes) / 1048576) TotalSpace")
    q1 = (q1 + "  from  dba_data_files")
    q1 = (q1 + " group by tablespace_name) df,")
    q1 = (q1 + " (select round(sum(bytes)/(1024*1024)) totalusedspace, tablespace_name")
    q1 = (q1 + "  from  dba_segments")
    q1 = (q1 + " group by tablespace_name) tu")
    q1 = (q1 + " where df.tablespace_name = tu.tablespace_name(+)  order by 5")
    return q1


def query_data_file(tb_name):
    q3 = ("SELECT FILE_NAME, BYTES/1024/1024/1024 FROM DBA_DATA_FILES ")
    q3 = (q3 + " WHERE TABLESPACE_NAME='")
    q3 = (q3 + tb_name + "' order by FILE_ID ")
#    print(q3)
    return q3


def query_diskgroup(DG):
    temp_name = (DG.split("+"))
    DG = temp_name[1]
    q = ("SELECT FREE_MB FROM V$ASM_DISKGROUP")
    q = (q + " WHERE NAME = '" + DG + "'")
    return q


def query_add_datafile(tablespace_name, datafile_size):
    query = ("ALTER TABLESPACE ")
    query = (query + tablespace_name)
    query = (query + " ADD DATAFILE SIZE " + datafile_size)
    query = (query + "M AUTOEXTEND ON NEXT 1G MAXSIZE UNLIMITED")
    return query


def work_on_tablespace(ORACLE_SID, USER_NAME):
    user = USER_NAME
    pw = "CIN2020#hq543#"
    hostvip = (ORACLE_SID + "vip")
    dns_tns = cx_Oracle.makedsn(hostvip, '1528', ORACLE_SID)
    con = cx_Oracle.connect(user, pw, dns_tns)
    cur = con.cursor()
    query_1 = query()
    cur.execute(query_1)
    table_p = PrettyTable(['Tablespace', 'Used MB', 'Free MB', ' Total MB', 'Pct. Free'])
    for row in cur:
        table_p.add_row(row)
    table_p.align = "r"
    print(table_p)
    if P_Version == "2":
        tb_name = raw_input(" \n Quel est le tablespace avec problème d'espace : ")
    else:
        tb_name = input("\n Quel est le tablespace avec problème d'espace : ")
    flag = 0
    print(tb_name)
    query_2 = ('select TABLESPACE_NAME from dba_tablespaces')
    cur.execute(query_2)
    for row_2 in cur:
        if row_2[0] == tb_name:
            flag = 1
    if flag == 1:
        print(" \n Valide tablespace " + tb_name)
        query_3 = query_data_file(tb_name)
        cur.execute(query_3)
        table_datafile = PrettyTable(['Datafile', 'Size G'])
        for row_3 in cur:
            table_datafile.add_row(row_3)
            datafile_name = row_3[0]
        print(table_datafile)
    else:
        print("\n Invalide tablespace " + tb_name)
    cur.close()
    con.close()
    return(tb_name, datafile_name)


def check_disk_group(ORACLE_SID, USER_NAME, DG, datafile_size):
    user = USER_NAME
    pw = "CIN2020#hq543#"
    hostvip = (ORACLE_SID + "vip")
    dns_tns = cx_Oracle.makedsn(hostvip, '1528', ORACLE_SID)
    con_2 = cx_Oracle.connect(user, pw, dns_tns)
    cur_2 = con_2.cursor()
    query = query_diskgroup(DG)
    cur_2.execute(query)
    for row in cur_2:
        actual_size = int(row[0])
    diskpace_dispo = actual_size - int(datafile_size)
    if diskpace_dispo > (int(datafile_size) * 2):
        flag = True
    else:
        flag = False
    print(flag)
    return flag


def create_add_df_file(USER_NAME, query):
    file = os.popen("touch /tmp/to_add_df.sh")
    file = open("/tmp/to_add_df.sh", "w")
    file.write("sqlplus -s " + USER_NAME + "/" + "CIN2020#hq543#" + " <<EOF\n")
    file.write("whenever sqlerror exit sql.sqlcode;\n")
    file.write("set heading off\n")
    file.write("spool " + USER_NAME +".log append \n")
    file.write(query + ";\n")
    file.write("exit; \n")
    file.write("/")
    file.write("\nEOF")
    file.close()


def adding_datafile(ORACLE_SID, USER_NAME, tablespace_name, datafile_size):
    query = query_add_datafile(tablespace_name, datafile_size)
    print("\n\n La requête ci-dessous sera exécutée: \n\n")
    print(query)
    answer = raw_input("\n\n Êtes-vous sûr : (1) Oui | (0) No ")
    flag = 0
    if answer == "1":
        create_add_df_file(USER_NAME, query)
        string_1 = ("sh /tmp/to_add_df.sh")
        f = os.popen(string_1)
        for line in f:
            print(line)
        print("Avez-vous une erreur à signaler")
        flag = raw_input("\n\n  (1) Oui | (0) No ")
        if flag == "0":
            print ("\n Vérifiez le fichier log \n \n")
        else:
            print(" \n Veuillez escalader")
    else:
        print("\n Veuillez escalader")


def add_data_file(tablespace_name, datafile_name, ORACLE_SID, USER_NAME):
    print("\n Quelle est la taille du Datafile")
    print("\n (1) 1G")
    print("\n (2) 10G")
    print("\n (3) 30G")
    print("\n (4) Outre, SVP scalader")
    size_answer = raw_input(" \n sélectionnez votre option : ")
    if size_answer == "1":
        datafile_size = "1024"
    elif size_answer == "2":
        datafile_size = "10240"
    elif size_answer == "3":
        datafile_size = "30000"
    else:
        print("SVP scalader")
    if (datafile_name.find("+") != -1):
        temp_name = (datafile_name.split("/"))
        DG = temp_name[0]
        if (check_disk_group(ORACLE_SID, USER_NAME, DG, datafile_size)):
            adding_datafile(ORACLE_SID, USER_NAME, tablespace_name, datafile_size)
        else:
            print("pas assez d'espace, veuillez escalader")
    else:
        print("\n No ASM, Veuillez escalader")


def tablespace_issues(ORACLE_SID, USER_NAME):
    string_4 = ("ora_pmon_"+ORACLE_SID)
    if checkIfProcessRunning(string_4):
#        print('\n Valid database \n ')
        tablespace_name, datafile_name = work_on_tablespace(ORACLE_SID, USER_NAME)
#        print(datafile_name)
        print(" \n Voulez-vous ajouter un datafile")
        ans = raw_input("(1) Oui / (0) No: ")
        print(ans)
        if ans == "1":
            add_data_file(tablespace_name, datafile_name, ORACLE_SID, USER_NAME)
        else:
            print(" \n Si nécessaire, escalade")
    else:
        print('invalid database')


def banner(text, ch='=', length=78):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    return banner


def print_menu(ORACLE_SID):

    print(banner(("OS : " + Current_os), " "))
    print(banner(("Python : " + P_Version), " "))
    print(banner(("Server name : " + hostname), " "))
    print(banner(("DB : " + ORACLE_SID), " "))
    print(banner(("User : " + username), " "))
    print(banner((""), " "))
    print(banner((""), " "))
    print(30 * "-", "MENU", 30 * "-")
    print("1. Vérifier le Filesystem")
    print("2. Vérifier un répertoire spécifique")
    print("3. Rechercher des fichiers > 1G")
    print("4. Tablespace incident")
    print("5  Sortir")
    print(67 * "-")


def menu_i(ORACLE_SID, USER_NAME):
    loop = True
    while loop:
        try:
            print_menu(ORACLE_SID)
            choice = int(input(" \n Entrez votre choix [1-5]: "))
            if choice == 1:
                focus_file_system()
            elif choice == 2:
                focus_on_dir(True)
            elif choice == 3:
                print("\n Nous recherchons des fichiers plus grands que 1G \n")
                focus_on_file()
            elif choice == 4:
                tablespace_issues(ORACLE_SID, USER_NAME)
            elif choice == 5:
                print("\n Sortir \n")
                loop = False
            else:
                print(" \n Oups! Ce n'était pas un nombre valide. Réessayer... \n ")
        except (RuntimeError, TypeError, NameError):
            print("\n\n Oups! Ce n'était pas un nombre valide. Réessayer...\n")


if __name__ == '__main__':
    ORACLE_SID = sys.argv[1]
    USER_NAME = sys.argv[2]
    menu_i(ORACLE_SID,USER_NAME)
