docs:
	python setup.py upload_docs --upload-dir docs/_build/html

update:
	python setup.py sdist upload --sign
	sudo pip install nntoolkit --upgrade

test:
	nosetests --with-coverage --cover-erase --cover-package nntoolkit --logging-level=INFO --cover-html

testall:
	make test
	cheesecake_index -n nntoolkit -v

count:
	cloc . --exclude-dir=docs,cover,dist,nntoolkit.egg-info

countc:
	cloc . --exclude-dir=docs,cover,dist,nntoolkit.egg-info,tests

countt:
	cloc tests