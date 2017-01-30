.phony: clean test

clean:
	find . -name *.pyc -delete

test:
	nosetests -P tests/unit/
