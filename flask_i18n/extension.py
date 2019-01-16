"""Flask Internationalization Extension module."""
import gettext as _gettext
import os

from flask import g, request
from werkzeug import http


class I18n():
    """Class to wrap Flask app and provide access to i18n convenience helpers."""

    def __init__(self, app=None, config=None):
        self.config = config
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):
        """Init Flask Extension."""
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        self.config.setdefault('I18N_DEFAULT_LOCALE', 'en')
        # Mapping of hacks to use when retrieving a translation
        self.config.setdefault('I18N_GETTEXT_HACKS', {})
        # List of language tags the app supports
        self.config.setdefault('I18N_LANGUAGE_TAGS', ['en'])

    def parse_accept_header(self, value):
        """Parse & store the Accept-Language header.

        Set it to be globally accessible for the current request.
        http://werkzeug.pocoo.org/docs/0.14/http/#werkzeug.http.parse_accept_header
        """
        accept_lang = http.parse_accept_header(value)
        g.language_tag = accept_lang.best_match(self.config['I18N_LANGUAGE_TAGS'])

        if not g.language_tag:
            cfg = self.config
            g.language_tag = cfg.get('BABEL_DEFAULT_LOCALE') or cfg['I18N_DEFAULT_LOCALE']

        return g.language_tag

    def gettext(self, domain, msg):
        """Custom gettext implementation that allows non-standard language tags.

        This is sometimes necessary for projects that have non-standard language tags
        because Flask-Babel & pybabel are unforgiving and translation projects sometimes
        choose weird language tags.
        """
        if 'language_tag' not in g:
            cfg = self.config
            default_lang_tag = cfg.get('BABEL_DEFAULT_LOCALE') or cfg['I18N_DEFAULT_LOCALE']

            g.language_tag = request.accept_languages.best_match(
                self.config['I18N_LANGUAGE_TAGS']) or default_lang_tag

        # gettext language tag hacks
        if g.language_tag in self.config['I18N_GETTEXT_HACKS'].keys():
            language_tag = self.config['I18N_GETTEXT_HACKS'][g.language_tag]
        else:
            language_tag = g.language_tag

        locale_dir = os.path.join(self.app.root_path, self.config['BABEL_TRANSLATION_DIRECTORIES'])

        translation = _gettext.translation(domain, localedir=locale_dir, languages=[language_tag])

        return translation.gettext(msg)
