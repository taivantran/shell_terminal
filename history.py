#!/usr/bin/env python3

def check_his(inp, his):
    inp_len = len(inp)
    result = ""
    index, flag = 0, 0
    while index < inp_len:
        if inp[index] == "!" and index + 1 < inp_len and inp[index + 1] != " ":
            if inp[index + 1].isdigit():
                index, tem = check_digit(inp, index + 1, his)
            elif inp[index + 1] == "!":
                if his == list():
                    tem = "!!"
                else:
                    index, tem = index + 2, his[::-1][0]
            elif inp[index + 1] == "-" and index + 2 < inp_len:
                index, tem = check_digit(inp, index + 2, his, "-")
            else:
                index, tem = check_character(inp, index + 1, his)
            if tem[0] == "!":
                print("intek-sh: %s: event not found" % tem)
                return False
            result += tem
            flag = 1
            continue
        result += inp[index]
        index += 1
    if flag:
        print(result)
    return result


def check_digit(str, start, his, sign=""):
    temp = ""
    while start < len(str):
        if not str[start].isdigit():
            break
        temp += str[start]
        start += 1
    temp = int(temp)
    if temp > len(his):
        return start, ("!%s%s" % (sign, temp))
    if sign == "-":
        return start, his[::-1][temp - 1]
    return start, his[temp - 1]


def check_character(str, start, his):
    temp = ""
    while start < len(str):
        if str[start] == " " or str[start] == "!":
                break
        temp +=  str[start]
        start += 1
    for i in his[::-1]:
        if i.startswith(temp):
            temp = i
            break
    if temp not in his:
        return start, ("!%s" % temp)
    return start, temp


def run_his(cmd, his):
    if len(cmd) == 1:
        for i in range(len(his)):
            print("%s  %s" %(str(i+1).rjust(5), his[i]))
    elif cmd[1] == "-c":
        his.clear()
    elif cmd[1] == "-d":
        if len(cmd) == 2:
            print("intek-sh: history: -d: option requires an argument")
        else:
            if cmd[2].isdigit() and 0 < int(cmd[2]) <= len(his):
                his.pop(int(cmd[2]) - 1)
            else:
                print("intek-sh: history: %s: history position out of range" % cmd[2])
    elif cmd[1].isdigit():
        if len(cmd) >= 3:
            print("intek-sh: history: too many arguments")
        else:
            his_l, his_s = len(his), 0
            if int(cmd[1]) <= his_l:
                his_s = his_l - int(cmd[1])
            for i in range(his_s, his_l):
                print("%s  %s" %(str(i+1).rjust(5), his[i]))
    else:
        print("intek-sh: history: %s: invalid option" %cmd[1])


if __name__ == "__main__":
    his = ["wfqjkfqjk", "cd", "ls", "ls -l", "-h"]
    loop = True
    while loop:
        inp = input()
        print(check_his(inp, his))
