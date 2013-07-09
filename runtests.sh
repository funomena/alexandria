coverage run --omit="venv/*,*/virtualenv/*,registration/*,*migrations/*,*tests*" manage.py test --settings=alexandria.settings.testing
TESTING_STATUS=$?
coverage html
coverage report
exit $TESTING_STATUS