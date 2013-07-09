if [[ $TRAVIS_BRANCH == 'master' ]]
	wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
	git remote add heroku git@heroku.com:alexandria-demo.git
	echo "Host heroku.com" >> ~/.ssh/config
	echo "   StrictHostKeyChecking no" >> ~/.ssh/config
	echo "   CheckHostIP no" >> ~/.ssh/config
	echo "   UserKnownHostsFile=/dev/null" >> ~/.ssh/config 
	heroku keys:clear
	yes | heroku keys:add
	heroku run python manage.py migrate --settings=alexandria.settings.heroku
fi