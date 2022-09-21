format-python:
	# Sort
	cd src/python/webserver; python -m isort .

	# Format
	cd src/python/webserver; python -m black --target-version py38 .
