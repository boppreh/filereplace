filereplace
===========

Utility to easily replace patterns in files. Can be used as a library or an
interactive program.

The two main functions are `update` and `replace`. The basic idea is that
`update` runs a function over the contents of a file and replaces it with the
funtion's return. `replace` uses a regular pattern and replacement string
system to modify files.
 
Both can trivially operate on whole directories, recursively or not.


`update(operation, path, recursive=False, line_by_line=False)`
-----

    Executes 'operation' for each file specified, passing as argument the
    contents of the file and replacing it with the value returned. Returns the
    path of all files updated.

    If path is a directory, this updates all files under that directory. If
    'recursive' is True, it updates all files in deeper directories too,
    recursively.

    If 'line_by_line' is True, 'operation' is called for each line in each file
    instead of the entire contents at once.


`replace(pattern, replacement, path, recursive=False, regex=False)`
-----

    Finds and replaces a pattern in each file specified. Returns the path of
    all files updated.

    If path is a directory, this updates all files under that directory. If
    'recursive' is True, it updates all files in deeper directories too,
    recursively.

    If 'regex' is true, pattern and replacement are treated as Regular
    Expressions. The syntax for the replacement is the same of the 're.sub'
    function (http://docs.python.org/2/library/re.html#re.sub)
