"""Test the i18n extension module."""
import unittest
from unittest.mock import patch

from flask import Flask, g

from flask_i18n import I18n  # isort:skip


def create_app():
    """Create a Flask app for context."""
    app = Flask(__name__)
    i18n = I18n()
    i18n.init_app(app)
    return app


class TestI18n(unittest.TestCase):
    """Test I18n class."""

    def setUp(self):
        """Set up tests."""
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Tear down tests."""
        self.ctx.pop()

    def test_default_config(self):
        """Test the default configs."""
        i18n = I18n(self.app)
        self.assertEqual(i18n.config['I18N_LANGUAGE_TAGS'], ['en'])
        self.assertEqual(i18n.config['I18N_GETTEXT_HACKS'], {})

    def test_custom_app_config(self):
        """Test custom configs set on app."""
        self.app.config['I18N_LANGUAGE_TAGS'] = ['es']
        self.app.config['I18N_GETTEXT_HACKS'] = {'en': 'es'}

        i18n = I18n(self.app)
        self.assertEqual(i18n.config['I18N_LANGUAGE_TAGS'], ['es'])
        self.assertEqual(i18n.config['I18N_GETTEXT_HACKS'], {'en': 'es'})

    def test_custom_kwarg_config(self):
        """Test custom configs passed via kwargs."""
        config = {
            'I18N_LANGUAGE_TAGS': ['en', 'es', 'pt'],
            'I18N_GETTEXT_HACKS': {'pt_BR': 'pt'},
        }

        i18n = I18n(self.app, config)
        self.assertEqual(i18n.config['I18N_LANGUAGE_TAGS'], ['en', 'es', 'pt'])
        self.assertEqual(i18n.config['I18N_GETTEXT_HACKS'], {'pt_BR': 'pt'})

    def test_init_app_with_config(self):
        """Test init app with passing kwarg config."""
        self.app = Flask(__name__)
        i18n = I18n()
        config = {
            'I18N_LANGUAGE_TAGS': ['en', 'es', 'pt'],
            'I18N_GETTEXT_HACKS': {'pt_BR': 'pt'},
        }
        i18n.init_app(self.app, config=config)

        self.assertEqual(i18n.config['I18N_LANGUAGE_TAGS'], ['en', 'es', 'pt'])
        self.assertEqual(i18n.config['I18N_GETTEXT_HACKS'], {'pt_BR': 'pt'})

    def test_parse_accept_header_defaults(self):
        """Test parsing the accept header with default configs."""
        i18n = I18n(self.app)
        header = 'da, en-gb;q=0.8, en;q=0.7'
        i18n.parse_accept_header(header)
        assert g.language_tag == 'en'

    def test_parse_accept_header_custom(self):
        """Test parsing the accept header with custom configs."""
        self.app.config['I18N_LANGUAGE_TAGS'] = ['da']
        i18n = I18n(self.app)

        header = 'da, en-gb;q=0.8, en;q=0.7'
        i18n.parse_accept_header(header)
        assert g.language_tag == 'da'

    def test_parse_accept_header_invalid(self):
        """Test parsing the accept header with default configs."""
        i18n = I18n(self.app)
        header = 'asdf'
        i18n.parse_accept_header(header)
        assert g.language_tag == 'en'

    @patch('flask_i18n.extension._gettext.translation')
    @patch('flask_i18n.extension.request')
    def test_gettext(self, mock_request, mock_gettext):
        """Test custom gettext wrapper + hacks."""
        mock_request.accept_languages.best_match.return_value = 'es_ES'

        self.app.config['I18N_LANGUAGE_TAGS'] = ['es']
        self.app.config['I18N_GETTEXT_HACKS'] = {'es_ES': 'es'}
        self.app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'i18n'
        i18n = I18n(self.app)

        i18n.gettext('domain', 'msg')
        mock_request.accept_languages.best_match.assert_called_once()
        mock_gettext.assert_called_once()

    @patch('flask_i18n.extension._gettext.translation')
    @patch('flask_i18n.extension.request')
    def test_gettext_no_hacks(self, mock_request, mock_gettext):
        """Test custom gettext wrapper without hacks."""
        mock_request.accept_languages.best_match.return_value = 'es_ES'

        self.app.config['I18N_LANGUAGE_TAGS'] = ['es']
        self.app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'i18n'
        i18n = I18n(self.app)

        i18n.gettext('domain', 'msg')
        mock_request.accept_languages.best_match.assert_called_once()
        mock_gettext.assert_called_once()
