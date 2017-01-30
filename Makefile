.phony: clean test

clean:
	find . -name *.pyc -delete
	rm -rf *.egg-info

test:
	nosetests -P tests/unit/
