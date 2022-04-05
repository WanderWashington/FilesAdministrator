import magic

from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

@deconstructible
class FileValidator(object):
    error_messages = {
     'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
     'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
     'content_type': "Files of type %(content_type)s are not supported.",
     'size_limit': "File size limit exceded",
    }

    def __init__(self, max_size=None, min_size=None):
        self.max_size = max_size
        self.min_size = min_size

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                   'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 
                                   'min_size', params)

        content_type = magic.from_buffer(data.read(), mime=True)
        data.seek(0)

        if content_type not in settings.FILE_TYPES.keys():
            params = { 'content_type': content_type }
            raise ValidationError(self.error_messages['content_type'],
                               'content_type', params)
        elif data.size > (settings.FILE_TYPES.get(content_type) * 1024):
            params = {'size_limit': (settings.FILE_TYPES.get(content_type) * 1024)}
            raise ValidationError(self.error_messages['size_limit'],
               'size_limit', params)


    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.max_size == other.max_size and
            self.min_size == other.min_size
        )