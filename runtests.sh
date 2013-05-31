coverage run --omit="venv/*,registration/*,*migrations/*,*tests*" manage.py test --settings=emubaby.settings.testing
coverage html
coverage report