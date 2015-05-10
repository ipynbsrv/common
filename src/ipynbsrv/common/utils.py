import importlib


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
    :param args: A string of optional arguments to pass to the class' init method (format: arg1=value,arg2=value).
    '''
    def __init__(self, module, klass, args=None):
        self._module = importlib.import_module(module)
        self._klass = klass
        self._args = ClassLoader.args_as_dict(args)

    '''
    Converts the arguments string (as per the defined format) into a dict.

    :param args: The arguments string. (i.e. 'version=1.18,arg2=3')
    '''
    @staticmethod
    def args_as_dict(args):
        args_dict = {}
        if args and isinstance(args, basestring):
            for arg in args.split(','):
                if arg.count('=') == 1:
                    key, value = arg.split('=', 1)
                    args_dict[key] = value
        return args_dict

    '''
    Returns an instance of the to be loaded class.

    :param args: Optional arguments to pass to the __init__ method (format: arg1=value,arg2=value).
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
