django-translatable-model
=========================

Provides a Language db Field which works with settings.LANGUAGES and defaults
to a *best match* of the current users language preference. The same best match
logic is used in the LanguageManager to automatically restrict the query to
returns results in the users language.
