import os
import shell


def para_expansion(st):
    ls = []
    em = ''
    kq = ''
    if st[0] != '$':
        ls += st.split('$')
        em += ls[0]
        ls = ['$' + i for i in ls[1:]]
        ls.insert(0, em)
    else:
        ls = st.split('$')[1:]
        ls = ['$' + i for i in ls]
    while '' in ls:
        ls.remove('')
    for i in ls:
        bien = os.path.expandvars(i)
        if '$' not in bien:
            kq += bien
    return kq


def tilde_expansion(ls):
    for i in range(len(ls)):
        # If the expansion fails or if the path does not begin with a tilde,
        # the path is returned unchanged.
        ls[i] = os.path.expanduser(ls[i])
        # current working directory
        if ls[i] == '~+' or '~+/' in ls[i]:
            ls[i] = ls[i].replace('~+', os.environ["PWD"])
        # old_ working directory
        elif ls[i] == '~-' or '~-/' in ls[i]:
            ls[i] = ls[i].replace('~-', os.environ["OLDPWD"])
    return ls
