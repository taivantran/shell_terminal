import subprocess as sub
import intek_sh
import shell


def find_subsitute(m):
    ls = []
    count = 0
    dem = 0
    if '``' in m:
        m = m.replace('``', '')
    while "`" in m:
        for i in range(len(m)):
            if "`" in m:
                if m[i] == "`":
                    j = i
                    while m[j+1] != "`":
                        j += 1
                    ls.append(m[i+1:j+1])
                    m = m.replace(m[i:j+2], str(count), 1)
                    count += 1
    return [ls, m.strip().split()]


def sub_command(cmd, his):
    st = ''
    chuoi = ' '.join(i for i in cmd)
    command = ''
    if chuoi.count('`') % 2 != 0:
        print("Invalid subsitute type")
        return None
    for i in chuoi:
        if i != '`':
            command += i
        else:
            break
    command = command.rstrip()
    flag = 0
    subsitute = find_subsitute(chuoi)
    ls_cmd = []
    for i in subsitute[0]:
        try:
            pr = sub.run(i.split(), stdout=sub.PIPE)
            pr = pr.stdout.decode().strip()
            ls_cmd.append(pr)
        except FileNotFoundError:
            print("intek-sh: " + i + ": command not found")
            return None
        except OSError:
            sub.run(['/bin/bash', '-c', i.split()[0]])
        except IndexError:
            pass

    if not ls_cmd:
        for i in range(len(subsitute[1])):
            try:
                subsitute[1][i] = int(subsitute[1][i])
            except ValueError:
                pass
            if type(subsitute[1][i]) == int:
                subsitute[1][i] = ''
    else:
        for i in range(len(ls_cmd)):
            for j in range(len(subsitute[1])):
                if str(i) == subsitute[1][j]:
                    subsitute[1][j] = ls_cmd[i]
    if subsitute[1] != ['']:
        intek_sh.process_cmd(subsitute[1], his)


    return cmd
