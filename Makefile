docs:
	python setup.py upload_docs --upload-dir docs/_build/html

localinstall:
	sudo -H python setup.py install

upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*

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

clean:
	rm -f *.hdf5 *.yml *.csv
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -type d -name "__pycache__" -delete
	sudo rm -rf build
	sudo rm -rf cover
	sudo rm -rf dist
	sudo rm -rf nntoolkit.egg-info