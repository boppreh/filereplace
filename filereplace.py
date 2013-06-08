import os
import fileinput
import re

def _update_lines_in_file(operation, file_path):
    """
    Executes 'operation' for every line in the given file, replacing the
    original line with the string returned by 'operation'. If 'operation'
    returns None, that line is left unchanged.
    """
    for line in fileinput.input([file_path], inplace=True):
        new_line = operation(line)

        if new_line is not None:
            print operation(line),
        else:
            print line

    return [file_path]

def _update_entire_file(operation, file_path):
    """
    Reads the contents of the given file, calls 'operation' with the contents
    as argument and, if the result is not None, replaces the contents of the
    file with the returned value.
    """
    with open(file_path, 'r') as file:
        contents = file.read()

    new_contents = operation(contents)

    if new_contents is None:
        return []

    with open(file_path, 'w') as file:
        file.write(new_contents)

    return [file_path]

def _update_single_file(operation, file_path, line_by_line=False):
    """
    Calls 'operation' on the contents of a given file, replacing the file
    contents with the value returned by the function if it's not None.

    If 'line_by_line' is True, 'operation' is called for every line. Otherwise,
    it is called with the entire contents of the file at once.
    """
    if line_by_line:
        return _update_lines_in_file(operation, file_path)
    else:
        return _update_entire_file(operation, file_path)

def _update_directory(operation, path, recursive=False, line_by_line=False,
                      extension=''):
    """
    Updates the contents of all files under a given directory.

    Returns the list of files changed.
    """
    files_updated = []

    for name in os.listdir(path):
        full_path = os.path.join(path, name)

        # Ignore directories if not recursive.
        if not recursive and os.path.isdir(full_path):
            continue

        results = update(operation, full_path, recursive, line_by_line,
                         extension)
        files_updated.extend(results)

    return files_updated

def update(operation, path, recursive=False, line_by_line=False,
           extension=''):
    """
    Executes 'operation' for each file specified, passing as argument the
    contents of the file and replacing it with the value returned. Returns the
    path of all files updated.

    If path is a directory, this updates all files under that directory. If
    'recursive' is True, it updates all files in deeper directories too,
    recursively.

    If 'line_by_line' is True, 'operation' is called for each line in each file
    instead of the entire contents at once.

    'extension' is an optional string with the extension of the files to be
    changed. Any file that doesn't end in that extension is ignored.
    """
    if not os.path.exists(path):
        raise IOError('Path does not exists: ' + path)

    if not path.endswith(extension):
        return []
        

    if os.path.isfile(path):
        return _update_single_file(operation, path, line_by_line)
    elif os.path.isdir(path):
        return _update_directory(operation, path, recursive, line_by_line,
                                 extension)
    else:
        assert False, 'Path is neither file nor directory.'

def replace(pattern, replacement, path, recursive=False, regex=False,
            extension=''):
    """
    Finds and replaces a pattern in each file specified. Returns the path of
    all files updated.

    If path is a directory, this updates all files under that directory. If
    'recursive' is True, it updates all files in deeper directories too,
    recursively.

    If 'regex' is true, pattern and replacement are treated as Regular
    Expressions. The syntax for the replacement is the same of the 're.sub'
    function (http://docs.python.org/2/library/re.html#re.sub)

    'extension' is an optional string with the extension of the files to be
    changed. Any file that doesn't end in that extension is ignored.
    """
    if regex:
        operation = lambda contents: re.sub(pattern, replacement, contents)
    else:
        operation = lambda contents: contents.replace(pattern, replacement)

    return update(operation, path, recursive, False, extension)

if __name__ == '__main__':
    # If executed as main script, act interactively. Only 'replace' feature
    # available because it's hard (and dangerous) to write a
    # replacement function with raw_input.

    print 'File Replace - Interactive Mode'
    print ''
    path = raw_input('Path (can be file or folder): ')
    pattern = raw_input('Regex pattern to replace: ')
    replacement = raw_input('Replacement: ')

    if os.path.isdir(path):
        recursive = raw_input('Operate recursively (y/N)? ') == 'y'
    else:
        recursive = False

    files_updated = replace(pattern,
                            replacement,
                            path,
                            recursive=recursive,
                            regex=True)

    print '\n\nFiles updated:'
    print '\n'.join(files_updated)
