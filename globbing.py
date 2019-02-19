import glob
import re
import os
import shell


def globbing(ls):
    all_f = os.listdir(os.environ["PWD"])
    dep = []
    tem = []
    newlist = []
    try:
        for i in range(len(ls)):
            tem = list(glob_filter(all_f, ls[i]))
            if tem != []:
                for k in tem:
                    if k not in ls:
                        ls.append(k)

            # process '.*' and '..*'
            if ls[i].startswith('.*'):
                dep = sub_glob(ls[i])
            elif ls[i].startswith('..*'):
                dep = sub_glob(ls[i][1:])
                dep.remove('.')
        newlist = [x for x in ls if (glob.glob(x) == []) or\
                  (len(glob.glob(x)) == 1 and '*' not in x)]
        if '..*' in newlist:
            newlist.remove('..*')
        newlist += dep
    except Exception as e:
        shell.export(['export', 'e=1'])
        pass
    return newlist


def sub_glob(i):
    tam = []
    command = []
    count_start = i.count("*")
    count_question = i.count("?")
    check = len(i) - 1
    if check == (count_start + count_question):
       if count_question < 1:
           tam.append(".")
           tam.append("..")
       elif count_question == 1:
           tam.append("..")
       elif count_question > 1:
           return tam
    else:
       tam.append(i)
    for j in tam:
       cmd = sorted(glob.glob(j))
       command += cmd
    return command


def glob2re(pat):
    """ Translate a shell PATTERN to a regular expression.

         quote meta-characters.
    """

    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            res = res + '.*'
            res = res + '[^/]*'
        elif c == '?':
            res = res + '.'
            res = res + '[^/]'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\','\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    # print(res + "'\Z(?ms)'")
    return res + '\Z(?ms)'


def glob_filter(names,pat):
    return (name for name in names if re.match(glob2re(pat),name))
