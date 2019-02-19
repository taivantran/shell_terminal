#!/usr/bin/env python3
import sys
import subprocess as sub
from intek_sh import *
import os
import shell
import re

org_out, org_err = sys.stdout, sys.stderr

def diff_list(lst1, lst2, delist):
    return [i for i in lst1 if i not in lst2 and i not in delist]


def check_pipe(lst):
    return [i for i in lst if i != ""]


def best(sub_com, num, out, err, flag=False):
    global org_out, org_in, org_err
    inp_r, error = None, None
    sample = [">", "<", ">>", "<<", "2>", "2>>"]
    dict1 = {">": "w", ">>": "a"}
    dict2 = {"2>": "w", "2>>": "a"}
    if num < 0:
        return None
    direct_lst = list()
    cmd = sub_com[num].split()
    cmd = modify_cmd(cmd)
    cmd = shell.execute_build_in_cmd(cmd)
    if cmd is None:
        return 1
    sys.stdout, sys.stderr = org_out, org_err
    for index in range(len(cmd)):
        if cmd[index] in sample:
            if index + 1 >= len(cmd):
                print("intek-sh: syntax error near unexpected token")
                return 1
            else:
                if cmd[index] in dict1:
                    sys.stdout = open(cmd[index + 1], dict1[cmd[index]])
                    flag = True
                elif cmd[index] == "<":
                    if os.path.exists(cmd[index + 1]):
                        with open(cmd[index + 1], "rb") as file:
                            content = file.read()
                            inp_r = content
                    else:
                        print("intek-sh: %s: No such file or directory" % cmd[index + 1])
                        error = 1
                elif cmd[index] == "<<":
                    loop = True
                    str = ""
                    while loop:
                        incont = input("> ")
                        if incont == cmd[index + 1]:
                            break
                        str += incont + "\n"
                    inp_r = str.encode("utf-8")
                elif cmd[index] in dict2:
                    sys.stderr = open(cmd[index + 1], dict2[cmd[index]])
                direct_lst.append(cmd[index + 1])
    inp = best(sub_com, num - 1, sys.stdout, sys.stderr)
    if error is not None:
        return 1
    if inp_r is not None:
        inp = inp_r
    cmd_lst = diff_list(cmd, direct_lst, sample)
    if num == len(sub_com) - 1 or flag is True:
        sub.run(cmd_lst, input=inp, stdout=sys.stdout, stderr=sys.stderr)
        sys.stdout, sys.stderr = out, err
        return 0
    pr = sub.run(cmd_lst, input=inp, stdout=sub.PIPE, stderr=sys.stderr)
    sys.stdout, sys.stderr = out, err
    return pr.stdout


def pipe_process(cmd):
    sub_com = check_pipe(cmd.split("|"))
    best(sub_com, len(sub_com) - 1, org_out, org_err)

if __name__ == "__main__":
        # cmd = "ls -l > quang1.txt"
        # cmd = "ls > quang1.txt | cat"
        # cmd = "ls -al > quang1.txt > quang2.txt"
        # cmd = "grep h < quang1.txt > result"
        # cmd = "ls -l note.txt quang.txt >> t1 2> t"
        # cmd = "ls | grep q > quang1.txt"
        # => If no quang1.txt => wrong!
        # cmd = "grep q < quang.txt | grep 1"
        # cmd = "cat << end < quang.txt"
        # cmd = "echo * | grep p"
        # cmd = "ls"
        # cmd = "ls | grep u | cat"
        # cmd = "ls < huhu| cat < haha"
        cmd = "ls <quang.txt"
        pipe_process(cmd)
