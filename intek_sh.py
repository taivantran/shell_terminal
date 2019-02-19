#!/usr/bin/python3
import shell
import globbing
import path_expansions
import sys
import history
from command_subsitute import *
import readline
from dynamic_cm import *


def check_sub(cmd):
    for i in cmd:
        if '`' in i:
            return True
    return False


def check_para(cmd):
    for i in cmd:
        if '=' not in i:
            return False
    return True


def change_exit_code(cmd):
    for i in range(len(cmd)):
        if cmd[i] == '$?':
            cmd[i] = '$e'


def process_cmd(cmd, his):
    change_exit_code(cmd)
    if check_sub(cmd):
        sub_command(cmd, his)
    elif check_para(cmd):
        cmd.insert(0, 'export')
        shell.export(cmd)
    elif 'printenv' in cmd:
        shell.printenv(cmd)
    elif 'history' in cmd:
        print(cmd)
        history.run_his(cmd, his)
    elif 'cd' in cmd:
        modify_cmd(cmd)
        shell.cd_code(cmd)
    elif 'exit' in cmd:
        shell.exit_code(cmd)
    elif 'export' in cmd:
        shell.export(cmd)
    elif 'unset' in cmd:
        shell.unset(cmd)
    else:
        shell.run_file(cmd)


def modify_cmd(cmd):
    cmd = path_expansions.tilde_expansion(cmd)
    cmd = globbing.globbing(cmd)
    cmd = [path_expansions.para_expansion(i) for i in cmd]
    return cmd


def main():
    command, temp = None, None
    his_list = list()
    vocabulary = set(get_cmd())
    readline.set_completer(make_completer(vocabulary))
    readline.parse_and_bind('tab: complete')

    while command != 'exit':
        try:
            usr_input = input('intek-sh$ ')
            if usr_input:
                usr_input = history.check_his(usr_input, his_list)
                if usr_input is False:
                    continue
                elif usr_input != temp:
                    his_list.append(usr_input)
                    temp = usr_input
                usr_input = usr_input.split()
                usr_input = process_cmd(usr_input, his_list)
                # usr_input = sub_command(usr_input, his_list)
        except EOFError:
            shell.exit_code([1])
        # ctrl + C
        except KeyboardInterrupt:
            print()
            shell.export(['export', 'e=130'])
            continue


if __name__ == '__main__':
    main()
