.PHONY: record delete

record:
	python3 loud-detector/record.py

delete:
	python3 loud-detector/deletefiles.py