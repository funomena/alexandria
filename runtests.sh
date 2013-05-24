coverage run --omit="venv/*,registration/*,*migrations/*,*tests*" manage.py test
coverage html
coverage report