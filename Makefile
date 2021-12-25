SHELL:=/bin/bash

all: clean buildthemes buildplankthemes

buildthemes:
	@echo "Building desktop themes"
	python3 generate-themes.py All
	
buildplankthemes:
	@echo "Building plank themes"
	mkdir -p usr/share/plank/themes
	@wait
	cp -Rv plank-themes/* usr/share/plank/themes/

clean:
	rm -rf usr __pycache__
	@echo "Remove generated css files."
	for f in `find ./src -type f -name '*.css'`; do \
		rm -f $$f; \
	done
