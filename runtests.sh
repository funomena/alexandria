coverage run --omit="venv/*,*/virtualenv/*,registration/*,*migrations/*,*tests*" manage.py test --settings=emubaby.settings.testing
TESTING_STATUS=$?
coverage html
coverage report
exit $TESTING_STATUS