from optparse import OptionParser

class ExtendedOptionParser(OptionParser):
    defaults = None

    def __init__(self, defaults, *args, **kwargs):
        # OptionParser is old-fashioned class, so super() is not applicable
        OptionParser.__init__(self, *args, **kwargs)
        self.defaults = defaults

    def add_option_with_default(self, *args, **kwargs):
        ret = None

        key = kwargs['dest']
        if key in self.defaults:
            ret = self.add_option(*args, default=self.defaults[key], **kwargs)
        else:
            ret = self.add_option(*args, **kwargs)

        return ret
