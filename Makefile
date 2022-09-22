format-python:
	# Sort
	cd src/python; python -m isort .

	# Format
	cd src/python; python -m black --target-version py38 .
