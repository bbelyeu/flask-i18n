# Flask-I18n

[![Build Status](https://travis-ci.org/bbelyeu/flask-i18n.svg?branch=master)](https://travis-ci.org/bbelyeu/flask-i18n)
[![Coverage Status](https://coveralls.io/repos/github/bbelyeu/flask-i18n/badge.svg?branch=master)](https://coveralls.io/github/bbelyeu/flask-i18n?branch=master)

## Requirements

This project requires Python 3.6 and Flask 0.12

## Installation

To install it, simply run

    pip install flask-i18n

## Usage

Import it and wrap app

    from flask import Flask
    from flask_i18n import I18n

    app = Flask(__name__)
    i18n = I18n(app)

The `I18N_DEFAULT_LOCALE` config variable is available to use in cases where the language
tag can't be determined from the Accept-Language header. It defaults to `en`.

You can use `I18N_LANGUAGE_TAGS` in config to setup what language tags your app supports.
Then parsing the `Accept-Language` header with the `parse_accept_header` method will use that list
to get the best available match and store it in the Flask globals var `g` accessible under
`g.language_tag`.

This extension also exposes a `gettext` method which can be used to wrap the builtin gettext
conveniently. It will use the best match of the `Accept-Language` header, and
[Flask-Babel](https://pythonhosted.org/Flask-Babel/) configuration setting
`BABEL_TRANSLATION_DIRECTORIES` to pull the correct translation from your project's gettext files.

It also allows for custom gettext language tag mapping since for flexibility.
For example if you want `pt` to map to `pt_BR` instead of `pt_PT`, you can setup config like

    I18N_GETTEXT_HACKS = {'pt': 'pt_BR'}

This accomodates non-standard language tag usage which gives `pybabel` major issues.

## Development

This project was written and tested with Python 3.6.

On a mac you can use the following commands to get up and running.
``` bash
brew install python3
```
otherwise run
``` bash
brew upgrade python3
```
to make sure you have an up to date version.

This project uses [pipenv](https://docs.pipenv.org) for dependency management. Install pipenv
``` bash
pip3 install pipenv
```

setup the project env
``` base
pipenv install --three --dev
```

create a .env file using this sample
``` bash
export PYTHONPATH=`pwd`
```

now load virtualenv and any .env file
```bash
pipenv shell
```

### Running tests

``` bash
./linters.sh && coverage run --source=flask_i18n/ setup.py test
```

### Before committing any code

We have a pre-commit hook which should be setup.
You can symlink it to run before each commit by changing directory to the repo and running

``` bash
cd .git/hooks
ln -s ../../pre-commit pre-commit
```
