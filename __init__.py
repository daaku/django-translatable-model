# coding: utf-8

from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import get_language


def best_languange(lang=None):
    """
    Provides the best language for the current user from the set of known
    languages if possible, otherwise the best language for the default
    LANGUAGE_CODE. With the Locale middleware enabled, this is probably not
    necessary. But without it, Django will not do the matching for us.

    """

    current = lang or get_language()
    available = [c for c, n in settings.LANGUAGES]
    if current in available:
        return current
    short = current[:2]
    if short in available:
        return short
    return best_languange(settings.LANGUAGE_CODE)

class LanguageField(models.CharField):
    """
    Provides a Language fields that works with the rest of the django i18n
    machinery.

    """

    def __init__(self, *args, **kwargs):
        defaults = {
            'max_length': 5,
            'default': best_languange,
            'choices': settings.LANGUAGES,
            'db_index': True,
        }
        defaults.update(kwargs)
        super(LanguageField, self).__init__(*args, **defaults)

class LanguageManager(models.Manager):
    def get_query_set(self):
        """
        Overrides the default ``QuerySet`` to only include rows
        with the current best language.

        """
        return (super(LanguageManager, self).
                get_query_set().
                filter(language__exact=best_languange))
