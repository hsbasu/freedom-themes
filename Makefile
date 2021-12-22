all: clean buildthemes

buildthemes:
	@echo "Building the themes"
	python3 generate-themes.py All

clean: SHELL:=/bin/bash
clean:
	rm -rf usr __pycache__
	@echo "Remove generated css files."
	for f in `find ./src -type f -name '*.css'`; do \
		rm -f $$f; \
	done
