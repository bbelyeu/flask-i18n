"""Add basic i18n functionality for APIs built as Flask apps."""
from setuptools import setup

setup(
    name='flask-i18n',
    version='1.0.0',
    url='https://github.com/bbelyeu/flask-i18n',
    download_url='https://github.com/bbelyeu/flask-i18n/archive/1.0.1.zip',
    license='MIT',
    author='Brad Belyeu',
    author_email='bradleylamar@gmail.com',
    description='Add basic i18n functionality for APIs built as Flask apps.',
    long_description=__doc__,
    packages=['flask_i18n'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords=['flask', 'i18n'],
    test_suite='flask_i18n.tests',
)
