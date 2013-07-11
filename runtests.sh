coverage run --omit="venv/*,*/virtualenv/*,registration/*,*migrations/*,*tests*,*pkg_resources*" manage.py test --settings=alexandria.settings.testing
TESTING_STATUS=$?
coverage html
coverage report
exit $TESTING_STATUS