import os
import subprocess
import pipe

def execute_f_python(filepath):
    try:
        subprocess.run(filepath)
    # ---------check lai. tren he thong----he thong phai tu trai loi~
    except PermissionError:
        print('intek-sh: ' + filepath + ': Permission denied')
    # ~~~~~~~~~~~~~~~~~~ nhu tren --------------
    except FileNotFoundError:
        print("intek-sh: " + filepath + ": No such file or directory")
    except OSError:
        subprocess.run(['/bin/bash', '-c', filepath])


def execute_build_in_cmd(cmd):
    try:
        PATH = os.environ['PATH'].split(':')
    except KeyError:
        print("intek-sh: " + cmd[0] + ": command not found")
        return None
    for item in PATH:
        if os.path.exists(item+'/'+cmd[0]):
            return [item+'/'+cmd.pop(0)]+cmd
    print("intek-sh: " + cmd[0] + ": command not found")


def run_file(type_in):
    if os.path.isfile(type_in[0]) or './' in (type_in[0]):
        execute_f_python(type_in[0])
    elif os.path.isdir(type_in[0]):
        print("intek-sh: " + type_in[0] + ": Is a directory")
    else:
        pipe.pipe_process(" ".join(type_in))


def execute_f_python(filepath):
    try:
        subprocess.run(filepath)
    except PermissionError:
        print('intek-sh: ' + filepath + ': Permission denied')
        export(['export', 'e=126'])
    except FileNotFoundError:
        print("intek-sh: " + filepath + ": No such file or directory")
        export(['export', 'e=127'])
    except OSError:
        subprocess.run(['/bin/bash', '-c', filepath])
        export(['export', 'e=0'])


def execute_build_in_cmd(cmd):
    if cmd:
        try:
            PATH = os.environ['PATH'].split(':')
        except KeyError:
            print("intek-sh: " + cmd[0] + ": command not found")
            export(['export', 'e=127'])
            return None
        for item in PATH:
            if os.path.exists(item+'/'+cmd[0]):
                export(['export', 'e=0'])
                return [item+'/'+cmd.pop(0)]+cmd
        print("intek-sh: " + cmd[0] + ": command not found")
        export(['export', 'e=127'])
        return None
    else:
        print("Not implemented yet")
        export(['export', 'e=1'])


def change_exit_code(cmd):
    for i in range(len(cmd)):
        if cmd[i] == '$?':
            cmd[i] = '$e'


def run_file(type_in):
    if os.path.isfile(type_in[0]):
        execute_f_python(type_in[0])
    elif os.path.isdir(type_in[0]):
        print("intek-sh: " + type_in[0] + ": Is a directory")
    else:
        pipe.pipe_process(" ".join(type_in))


def printenv(cmd):
    if cmd == ['printenv']:
        for key in os.environ:
            print(key + '=' + os.environ[key])
    elif len(cmd) == 2:
        try:
            print(os.environ[cmd[1]])
            export(['export', 'e=0'])
        except KeyError:
            export(['export', 'e=1'])
            pass
    else:
        for i in cmd[1:]:
            try:
                print(os.environ[i])
                export(['export', 'e=0'])
            except KeyError:
                export(['export', 'e=1'])
                pass


def exit_code(cmd):
    print('exit')
    try:
        code = int(cmd[1])
        exit(code)
    except ValueError:
        print('intek-sh: exit:')
        export(['export', 'e=128'])
        exit()
    except IndexError:
        exit(0)


def unset(cmd):
    if cmd == ['unset']:
        pass
    else:
        cmd = cmd[1:]
        for variable in cmd:
            if variable in os.environ.keys():
                del os.environ[variable]
            else:
                return


def cd_code(cmd):
    if cmd == ['cd']:
        try:
            os.chdir(os.environ["HOME"])
            export(['export', 'e=0'])
        except KeyError:
            print("intek-sh: cd: HOME not set")
            export(['export', 'e=1'])
    else:
        if os.path.exists(cmd[1]):
            try:
                os.environ["OLDPWD"] = os.environ["PWD"]
                os.chdir(os.path.abspath(cmd[1]))
                os.environ["PWD"] = os.getcwd()
                export(['export', 'e=0'])
            except NotADirectoryError:
                print("bash: cd: " + cmd[1] + ": Not a directory")
                export(['export', 'e=1'])
        else:
            print("intek-sh: cd: " + cmd[1] + ": "
                  "No such file or directory")
            export(['export', 'e=127'])



def export(cmd):
    if cmd == ['export']:
        export(['export', 'e=0'])
        pass
    else:
        lst_cmd = cmd[1:]
        for variable in lst_cmd:
            if '=' not in variable:
                os.environ[variable] = ''
            else:
                variable = variable.split('=')
                os.environ[variable[0]] = variable[1]
