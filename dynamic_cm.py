import readline
from glob import glob
import os



def make_completer(vocabulary):
    def custom_complete(text, state):
        # None is returned for the end of the completion session.
        results = [x for x in vocabulary if x.startswith(text)] + [None]
        # A space is added to the completion since the Python readline doesn't
        # do this on its own. When a word is fully completed we want to mimic
        # the default readline library behavior of adding a space after it.
        # return results[state] + " "

        matches = []
        ''' Simplistic parsing of the command-line so far. We want to know
         if the user is still entering the command, or if the command is
         already there and now we have to complete the subcommand. '''
        linebuf = readline.get_line_buffer()
        parts = linebuf.split()

        if len(parts) >= 1 and linebuf.endswith(' '):
            ''' If we're past the first part and there is whitespace at
            the end of the buffer, it means we're already completing the
            next part. '''
            parts.append('')

        if len(parts) is 0:
            ''' do nothing when the user doesn't enter anything '''
            matches.append(None)
            return matches[state]

        elif len(parts) is 1:
            ''' If the completion happens on the first word,
                commands are suggested'''
            command = parts[0]
            if '/' in command or '*' in command:
                ''' list all files and folders in '.' directory '''
                matches = list_dir_for_anythingElse(text)
                matches.append(None)
                # matches.append(None)
                if len(matches) > 2:
                  # print(matches)
                  ''' if there is more than 1 result matched '''
                  return matches[state]
                elif len(matches) == 2:
                  # print(matches)
                  ''' just 1 result matched '''
                  return matches[state]
            for key in vocabulary:
                if key.startswith(text):
                    matches.append(key + ' ')
            matches.append(None)
            return matches[state]

        elif len(parts) >= 2:
            ''' otherwise files in the current directly are suggested.'''
            command = parts[0]

            if command == 'cd':
                ''' just list the present directories if command is cd '''
                matches = list_dir_for_cd(text)
                matches.append(None)
                return matches[state]
            else:
                ''' Treat 'file' specially, by looking for matching files
                in the current directory.'''
                matches = list_dir_for_anythingElse(text)
                matches.append(None)
                return matches[state]

    return custom_complete


def list_dir_for_anythingElse(text):
    ''' from_to: in case `./` or `../` in command -> strip them'''
    anythingElse_matches = []
    for filename in glob(text + '*'):
        if os.path.isdir(filename):
            anythingElse_matches.append(filename + '/ ')
        else:
            anythingElse_matches.append(filename + ' ')
    # including hidden files and folders
    for hidden_filename in glob(text + '.*'):
        if os.path.isdir(hidden_filename):
            anythingElse_matches.append(hidden_filename + '/ ')
        else:
            anythingElse_matches.append(hidden_filename + ' ')
    return anythingElse_matches



def get_cmd():
    ls_cm = ['printenv', 'cd', 'exit', 'printenv', 'export', 'unset']
    cmds = []
    for cm in os.environ["PATH"].split(':'):
        try:
            cmds = os.listdir(cm)
        except FileNotFoundError:
            pass
        for i in cmds:
            ls_cm.append(i)
    return ls_cm
