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


class ArticleLoader(Loader):

    """
    Article loader.

    """
    def find(self, directory):
        """
        Find all articles in a given directory.
        """
        files = listdir(directory)

        # Find all the files
        for filename in files:
            yield self.obj_class(join(directory, filename))
