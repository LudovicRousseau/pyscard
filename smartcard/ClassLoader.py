"""ClassLoader allows you to load modules from packages without
hard-coding their class names in code; instead, they might be
specified in a configuration file, as command-line parameters,
or within an interface.

Source: Robert Brewer at the Python Cookbook:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/223972

License: PSF license (http://docs.python.org/license.html).
"""


def get_mod(modulePath):
    """Import a module."""
    return __import__(modulePath, globals(), locals(), [''])


def get_func(fullFuncName):
    """Retrieve a function object from a full dotted-package name."""

    # Parse out the path, module, and function
    lastDot = fullFuncName.rfind(u".")
    funcName = fullFuncName[lastDot + 1:]
    modPath = fullFuncName[:lastDot]

    aMod = get_mod(modPath)
    aFunc = getattr(aMod, funcName)

    # Assert that the function is a *callable* attribute.
    assert callable(aFunc), u"%s is not callable." % fullFuncName

    # Return a reference to the function itself,
    # not the results of the function.
    return aFunc


def get_class(fullClassName, parentClass=None):
    """Load a module and retrieve a class (NOT an instance).

    If the parentClass is supplied, className must be of parentClass
    or a subclass of parentClass (or None is returned).
    """
    aClass = get_func(fullClassName)

    # Assert that the class is a subclass of parentClass.
    if parentClass is not None:
        if not issubclass(aClass, parentClass):
            raise TypeError(u"%s is not a subclass of %s" %
                            (fullClassName, parentClass))

    # Return a reference to the class itself, not an instantiated object.
    return aClass
