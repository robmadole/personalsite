from os.path import basename


class FilenameMatcher(object):

    """
    Extract meta information out of a filename.

    This class when created will examine the basename of the provided path,
    extract meta data, and set attributes on the instance for later use.

    """
    filename_pattern = None

    def __init__(self, path):
        self.path = path
        self.basename = basename(path)

        match = self.filename_pattern.match(self.basename)

        if not match:
            raise ValueError('Invalid filename {}'.format(self.basename))

        parts = match.groupdict()

        for key, val in parts.items():
            try:
                val = int(val)
            except:
                pass
            setattr(self, key, val)
