from regex import regex
from wtforms import ValidationError


def proper_regexp(regexp='', message=''):
    def _proper_regexp(form, field):
        if regex.fullmatch(regexp, str(field.data)) is None:
            raise ValidationError(message)

    return _proper_regexp
