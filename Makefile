.PHONY: all clean build_all upload local

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

ifeq ($(OS),Windows_NT)
SHELL=cmd
RM=del /Q /F
RRM=rmdir /Q /S
CP=copy
MKDIR=mkdir
TOUCH=copy nul
FixPath=$(subst /,\,$1)
ConditionalRmDir=if exist $(call FixPath,$1) (rmdir /q /s $(call FixPath,$1))
# this finds the first lilypond executable on the path, gets the directory, and works out how to run lilypond-book from there with our python
LILYPOND_DIR=$(shell cmd /E:ON /c set "FIRST=" & for /F "delims= eol=|" %%E in ('where lilypond.exe') do @if not defined FIRST (set FIRST=F & echo %%~dpE))
ifeq ($(realpath $(LILYPOND_DIR)\lilypond-book.py),)
    LILYPOND_BOOK=python $(LILYPOND_DIR)\lilypond-book
else
    LILYPOND_BOOK=python $(LILYPOND_DIR)\lilypond-book.py
endif
else
RM=rm -f
RRM=rm -f -r
CP=cp
MKDIR=mkdir -p
TOUCH=touch
FixPath=$1
ConditionalRmDir=if [ -d $1 ] ; then rm -r $1 ; fi
LILYPOND_BOOK=lilypond-book
endif

output_genshi=$(foreach filename,$(wildcard *.genshi.html),docs/$(filename:.genshi.html=.html))
output_lilypond_genshi=$(foreach filename,$(wildcard *.lilypond-genshi.html),docs/$(filename:.lilypond-genshi.html=.html))
output_sample_lilypond=$(foreach filename,$(wildcard samples/*.ly),docs/$(filename:.ly=.pdf) docs/$(filename))
output_svg=$(foreach filename,$(wildcard *.genshi.svg),docs/$(filename:.genshi.svg=.svg))
output_png=$(foreach filename,$(wildcard *.genshi.svg),docs/$(filename:.genshi.svg=.png))
output_css=$(foreach filename,$(wildcard css/*.css),docs/$(filename))
html_includes=header.html footer.html head_contents.html
# genshify_args="target=\"github_pages\""

all: build_all

build_all: chromaturn.ly $(output_css) $(output_genshi) $(output_lilypond_genshi) $(output_svg) $(output_png) $(output_sample_lilypond)

clean:
	$(RRM) docs
	$(RRM) tmp
	$(RM) chromaturn.ly

SAMPLES=docs/samples/.d
OUT=docs/.d
OUT_CSS=docs/css/.d
TMP=tmp/.d

%/.d:
	$(MKDIR) $(call FixPath,$(@D))
	$(TOUCH) $(call FixPath,$@)

.PRECIOUS: %/.d tmp/%.html

$(shell python ./pydeps -M > Makefile.pydeps)
include Makefile.pydeps

%.ly: %.genshi.ly
	python ./genshify -o $@ $< ${genshify_args}

docs/guitar-fretboard.svg: guitar_layout.py sticker-def.genshi.xml guitar-base.genshi.xml guitar-strings.genshi.xml

docs/piano-keyboard.svg: piano_layout.py

docs/%.svg: %.genshi.svg $(OUT)
	python ./genshify -o $@ $< ${genshify_args}

docs/%.png: docs/%.svg
	inkscape $< -o $@

docs/%.html: %.genshi.html $(html_includes) $(OUT)
	python ./genshify -o $@ $< ${genshify_args}

docs/%.txt: %.genshi.txt $(OUT)
	python ./genshify -o $@ $< ${genshify_args}

docs/css/%.css: css/%.css $(OUT) $(OUT_CSS)
	$(CP) $(call FixPath,$<) $(call FixPath,$@)

# Remove temporary files to ensure regeneration of lilypond pictures, since lilypond-book does its own incomplete dependency check
# include a temporary fix to copy the generated pngs into the docs/ directory, since this is not happening on lilypond 2.22
docs/%.html: tmp/%.html $(OUT) $(TMP)
	$(call ConditionalRmDir,docs/lily/)
	$(LILYPOND_BOOK) --lily-output-dir docs/lily/ --process "lilypond -dbackend=eps" --output docs/ $<
	python copy-lily-pngs.py
	$(call ConditionalRmDir,docs/lily/)

tmp/%.html: %.lilypond-genshi.html chromaturn.ly $(TMP)
	python ./genshify -o $@ $< ${genshify_args}

# We ensure that this is copied to the target directory, and actually compile from there
docs/samples/%.ly: samples/%.ly $(SAMPLES)
	$(CP) $(call FixPath,$<) $(call FixPath,$@)

docs/samples/%.pdf: docs/samples/%.ly $(SAMPLES) chromaturn.ly
	lilypond --pdf -o $(@:.pdf=) $<

# local: build_all
# 	$(MKDIR) ~/frasergo-website/frasergo-mezzanine/static/projects/harmonihue/
# 	rsync -avzP docs/ ~/frasergo-website/frasergo-mezzanine/static/projects/harmonihue/

# upload: build_all
# 	ssh longlake.frasergo.org "mkdir -p .virtualenv/frasergo/project/static/projects/harmonihue/"
# 	rsync -avzP docs/ longlake.frasergo.org:.virtualenv/frasergo/project/static/projects/harmonihue/

