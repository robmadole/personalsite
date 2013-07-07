from os import listdir
from os.path import join


class Loader(object):

    """
    Factory class used to get specific loaders.

    """
    # The class used when creating objects found.
    obj_class = None

    @classmethod
    def _lookup_loader(cls, obj_class):
        name = '{}Loader'.format(obj_class.__name__)

        return globals()[name]

    def __new__(cls, obj_class, *args, **kwargs):
        specific_cls = cls._lookup_loader(obj_class)
        instance = super(Loader, specific_cls).__new__(specific_cls)
        instance.obj_class = obj_class

        return instance


class DirectoryFinder(object):

    """
    Find objects in a directory of files.

    """
    def find(self, directory):
        """
        Find all objects in a given directory.
        """
        files = listdir(directory)

        # If our object has a clear_cache method call that to prepare
        # for a new set of objects.
        try:
            self.obj_class.clear_cache()
        except AttributeError:
            pass

        # Find all the files
        for filename in files:
            yield self.obj_class(join(directory, filename))


class ArticleLoader(Loader, DirectoryFinder):

    """
    Article loader.

    """
    pass


class BookmarkLoader(Loader, DirectoryFinder):

    """
    Bookmark loader.

    """
    pass
