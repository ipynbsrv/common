import ast
from grp import getgrnam
import importlib
import os
from pathlib import Path
from pwd import getpwnam
import shutil


class ClassLoader(object):

    """
    ClassLoader instances can be used to load Python classes at runtime by name.

    The typical use-case is the host API command-line tool that supports setting a custom
    container backend via arguments.
    """

    def __init__(self, module, klass, args=None):
        """
        Initialize a new instance that will load the given class from the given module.

        :param module: The absolute path of the module where the class is located.
        :param klass: The class' to load name.
        :param args: A string of optional arguments to pass to the class' init method (format: { "arg1": "value", "arg2" : "value" }).
        """
        self._module = importlib.import_module(module)
        self._klass = klass
        self._args = ClassLoader.args_as_dict(args)

    @staticmethod
    def args_as_dict(args):
        """
        Convert the arguments string (as per the defined format) into a dict.

        :param args: The arguments string in json form. (i.e. '{ "version": "1.18" , "arg2": "3"}' )
        """
        args_dict = {}
        if args and isinstance(args, basestring):
            try:
                args_dict = ast.literal_eval(args)
            except SyntaxError as e:
                print("args have a invalid format. Please use json format (args provided: %s)" % args)
                raise e
        elif isinstance(args, dict):
            args_dict = args
        elif args:
            raise ValueError("Only dictionaries and strings can be converted. %s given." % type(args))

        return args_dict

    def get_instance(self, args=None):
        """
        Get an instance of the to be loaded class.

        :param args: Optional arguments to pass to the __init__ method (format: { "arg1": "value", "arg2" : "value" }).
        """
        arguments = self._args
        if args:
            arguments = ClassLoader.args_as_dict(args)
        klass = getattr(self._module, self._klass)
        if arguments:
            return klass(**arguments)
        else:
            return klass()

    @staticmethod
    def split(absolute_klass):
        """
        Split the input string into its package/module part and class name.

        :param absolute_klass: The absolute class name including the whole package/module path.
        """
        module, sep, klass = absolute_klass.rpartition('.')
        return (module, klass)


class FileSystem(object):

    """
    Helper class for filesystem operations.
    """

    def __init__(self, base_dir='.'):
        """
        Initialize a new FileSystem object with the given base directory.

        TODO: make base_dir a property because _path needs to be changed if changed.

        :param base_dir: The base directory (operations will be executed relatively to it).
        """
        self.base_dir = base_dir
        self._path = Path(base_dir)

    def exists(self, path='.'):
        """
        Check if the path exists.

        :param path: The path (relative to the base_dir) to check.
        """
        return (self._path / path).exists()

    def get_full_path(self, path='.'):
        """
        Get the full path as a posix string.

        :param path: The path to get the full posix path for.
        """
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).resolve().as_posix()

    def get_gid(self, path='.'):
        """
        Get the group ID of the provided path.

        :param path: The path to get the group ID for.
        """
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).stat().st_gid

    def get_group(self, path='.'):
        """
        Get the group name of the provided path.

        :param path: The path to get the group for.
        """
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).group()

    def get_mode(self, path='.'):
        """
        Get the access mode of the provided path.

        :param path: The path to get the group for.
        """
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).stat().st_mode

    def get_owner(self, path='.'):
        """
        Get the owner username of the provided path.

        :param path: The path to get the owner for.
        """
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).owner()

    def get_uid(self, path='.'):
        """
        Get the owner's ID of the provided path.

        :param path: The path to get the owner's ID for.
        """
        if not self.exists(path):
            raise IOError("Path does not exists.")

        return (self._path / path).stat().st_uid

    def is_dir(self, path='.'):
        """
        Check if the path is a directory or not (e.g. a file).

        :param path: The path to check.
        """
        if not self.exists(path):
            raise IOError("Path does not exist.")
        return (self._path / path).is_dir()

    def is_file(self, path='.'):
        """
        Check if the path is a file or not (e.g. a directory).

        :param path: The path to check.
        """
        if not self.exists(path):
            raise IOError("Path does not exist.")
        return (self._path / path).is_file()

    def mk_dir(self, dir_name='.'):
        """
        Create a directory with the given dir_name.

        :param dir_name: The name/path of the to be created directory (relative to the base_dir).
        """
        if self.exists(dir_name):
            raise IOError("Target path already exists.")

        created = (self._path / dir_name)
        created.mkdir()
        return FileSystem((self._path / created).resolve().as_posix())  # HACK: get_full_path raises error

    def rm_dir(self, dir_name='.'):
        """
        Remove the directory with the given dir_name.

        :param dir_name: The name/path of the to be removed directory (relative to the base_dir).
        """
        if not self.exists(dir_name):
            raise IOError("Path does not exist.")
        if not self.is_dir(dir_name):
            raise IOError("Path is not a directory.")

        (self._path / dir_name).rmdir()

    def rrm_dir(self, dir_name='.'):
        """
        Recursively remove the directory with the given dir_name.

        :param dir_name: The name/path of the to be removed directory (relative to the base_dir).
        """
        if not self.exists(dir_name):
            raise IOError("Path does not exist.")
        if not self.is_dir(dir_name):
            raise IOError("Path is not a directory.")

        shutil.rmtree(self.get_full_path(dir_name))

    def set_group(self, group, path='.'):
        """
        Set the path's group (by group name).

        :param group: The name of the group to set.
        :param path: The path to set the group on.
        """
        self.set_gid(getgrnam(group).gr_gid, path)

    def set_gid(self, gid, path='.'):
        """
        Set the path's group (by group ID).

        :param gid: The group's ID.
        :param path: The path to set the group on.
        """
        if not self.exists(path):
            raise IOError("Path does not exist.")

        os.chown(self.get_full_path(path), -1, gid)

    def set_mode(self, mode, path='.'):
        """
        Set the path's access mode.

        :param mode: The path's new access mode.
        :param path: The path on which the mode should be set.
        """
        if not self.exists(path):
            raise IOError("Path does not exist.")

        (self._path / path).chmod(mode)

    def set_owner(self, owner, path='.'):
        """
        Set the path's owner (by username).

        :param owner: The username of the new path owner.
        :param path: The path to set the owner on.
        """
        self.set_uid(getpwnam(owner).pw_uid, path)

    def set_uid(self, uid, path='.'):
        """
        Set the path's owner (by user ID).

        :param uid: The user's ID.
        :param path: The path to set the owner on.
        """
        if not self.exists(path):
            raise IOError("Path does not exist.")

        os.chown(self.get_full_path(path), uid, -1)
