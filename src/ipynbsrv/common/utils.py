import ast
from grp import getgrnam
import importlib
import os
from pathlib import Path
from pwd import getpwnam
import shutil


class ClassLoader(object):
    '''
    ClassLoader instances can be used to load Python classes at runtime by name.

    The typical use-case is the host API command-line tool that supports setting a custom
    container backend via arguments.
    '''

    '''
    Initializes a new instance that will load the given class from the given module.

    :param module: The absolute path of the module where the class is located.
    :param klass: The class' to load name.
    :param args: A string of optional arguments to pass to the class' init method (format: { "arg1": "value", "arg2" : "value" }).
    '''
    def __init__(self, module, klass, args=None):
        self._module = importlib.import_module(module)
        self._klass = klass
        self._args = ClassLoader.args_as_dict(args)

    '''
    Converts the arguments string (as per the defined format) into a dict.

    :param args: The arguments string in json form. (i.e. '{ "version": "1.18" , "arg2": "3"}' )
    '''
    @staticmethod
    def args_as_dict(args):
        args_dict = {}
        if args and isinstance(args, basestring):
            try:
                args_dict = ast.literal_eval(args)
            except SyntaxError as e:
                print("args have a invalid format. Please use json format (args provided: {0})".format(args))
                raise e
        elif isinstance(args, dict):
            args_dict = args
        elif args:
            raise ValueError("Only dictionaries and strings can be converted. %s given." % type(args))

        return args_dict

    '''
    Returns an instance of the to be loaded class.

    :param args: Optional arguments to pass to the __init__ method (format: { "arg1": "value", "arg2" : "value" }).
    '''
    def get_instance(self, args=None):
        arguments = self._args
        if args:
            arguments = ClassLoader.args_as_dict(args)
        klass = getattr(self._module, self._klass)
        if arguments:
            return klass(**arguments)
        else:
            return klass()

    '''
    Splits the input string into its package/module part and class name.

    :param absolute_klass: The absolute class name including the whole package/module path.
    '''
    @staticmethod
    def split(absolute_klass):
        module, sep, klass = absolute_klass.rpartition('.')
        return (module, klass)


class FileSystem(object):
    '''
    Helper class for filesystem operations.
    '''

    '''
    TODO: make base_dir a property because _path needs to be changed if changed
    '''
    def __init__(self, base_dir='.'):
        self.base_dir = base_dir
        self._path = Path(base_dir)

    '''
    Checks if the directory exists.

    :param dir_name: The directory (relative to the base_dir) to check.
    '''
    def exists(self, dir_name='.'):
        return (self._path / dir_name).exists()

    '''
    Returns the full path as a posix string.

    :param path: The path to get the full posix path for.
    '''
    def get_full_path(self, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).resolve().as_posix()

    '''
    Returns the group name of the provided path.

    :param path: The path to get the group for.
    '''
    def get_group(self, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).group()

    '''
    Returns the group ID of the provided path.

    :param path: The path to get the group ID for.
    '''
    def get_gid(self, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).stat().st_gid

    '''
    Returns the access mode of the provided path.

    :param path: The path to get the group for.
    '''
    def get_mode(self, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).stat().st_mode

    '''
    Returns the owner username of the provided path.

    :param path: The path to get the owner for.
    '''
    def get_owner(self, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).owner()

    '''
    Returns the owner's ID of the provided path.

    :param path: The path to get the owner's ID for.
    '''
    def get_uid(self, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).stat().st_uid

    '''
    Checks if the path is a directory or not (e.g. a file).

    :param dir_name: The directory to check.
    '''
    def is_dir(self, dir_name='.'):
        if not self.exists(dir_name):
            raise IOError("Path does not exist.")
        return (self._path / dir_name).is_dir()

    '''
    Checks if the path is a file or not (e.g. a directory).

    :param file_name: The file to check.
    '''
    def is_file(self, file_name='.'):
        if not self.exists(file_name):
            raise IOError("Path does not exist.")
        return (self._path / file_name).is_file()

    '''
    Creates a directory with the given dir_name.

    :param dir_name: The name/path of the to be created directory (relative to the base_dir).
    '''
    def mk_dir(self, dir_name='.'):
        if self.exists(dir_name):
            raise IOError("Target path already exists.")

        created = (self._path / dir_name)
        created.mkdir()
        return FileSystem(self.get_full_path(created.name))  # FIXME: raises dot not exist

    '''
    Removes the directory with the given dir_name.

    :param dir_name: The name/path of the to be removed directory (relative to the base_dir).
    '''
    def rm_dir(self, dir_name='.'):
        if not self.exists(dir_name):
            raise IOError("Path does not exist.")
        if not self.is_dir(dir_name):
            raise IOError("Path is not a directory.")

        (self._path / dir_name).rmdir()

    '''
    Recursively removes the directory with the given dir_name.

    :param dir_name: The name/path of the to be removed directory (relative to the base_dir).
    '''
    def rrm_dir(self, dir_name='.'):
        if not self.exists(dir_name):
            raise IOError("Path does not exist.")
        if not self.is_dir(dir_name):
            raise IOError("Path is not a directory.")

        shutil.rmtree(self.get_full_path(dir_name))

    '''
    Sets the path's group (by group name).

    :param path: The path to set the group on.
    :param group: The name of the group to set.
    '''
    def set_group(self, group, path='.'):
        self.set_gid(getgrnam(group).gr_gid, path)

    '''
    Sets the path's group (by group ID).

    :param path: The path to set the group on.
    :param gid: The group's ID.
    '''
    def set_gid(self, gid, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exist.")

        os.chown(self.get_full_path(path), -1, gid)

    '''
    TODO
    '''
    def set_mode(self, mode, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exist.")

        (self._path / path).chmod(mode)

    '''
    Sets the path's owner (by username).

    :param path: The path to set the owner on.
    :param owner: The username of the new path owner.
    '''
    def set_owner(self, owner, path='.'):
        self.set_uid(getpwnam(owner).pw_uid, path)

    '''
    Sets the path's owner (by user ID).

    :param path: The path to set the owner on.
    :param uid: The user's ID.
    '''
    def set_uid(self, uid, path='.'):
        if not self.exists(path):
            raise IOError("Path does not exist.")

        os.chown(self.get_full_path(path), uid, -1)
