.PHONY: all clean build_all upload local

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
testme := $(shell echo $(mkfile_path) > test.txt)
current_dir := $(dir $(mkfile_path))
testme2:= $(shell echo $(current_dir) >> test.txt)

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
LILYPOND_BOOK=python $(LILYPOND_DIR)\lilypond-book.py
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

output_genshi=$(foreach filename,$(wildcard *.genshi.html),out/$(filename:.genshi.html=.html))
output_lilypond_genshi=$(foreach filename,$(wildcard *.lilypond-genshi.html),out/$(filename:.lilypond-genshi.html=.html))
output_sample_lilypond=$(foreach filename,$(wildcard samples/*.ly),out/$(filename:.ly=.pdf) out/$(filename))
output_svg=$(foreach filename,$(wildcard *.genshi.svg),out/$(filename:.genshi.svg=.svg))
output_png=$(foreach filename,$(wildcard *.genshi.svg),out/$(filename:.genshi.svg=.png))
html_includes=header.html footer.html head_contents.html
genshify_args='target="mezzanine_include"'

all: build_all

build_all: chromaturn.ly $(output_genshi) $(output_lilypond_genshi) $(output_svg) $(output_png) $(output_sample_lilypond)

clean:
	$(RRM) out
	$(RRM) tmp
	$(RM) chromaturn.ly

SAMPLES=out/samples/.d
OUT=out/.d
TMP=tmp/.d

%/.d:
	$(MKDIR) $(call FixPath,$(@D))
	$(TOUCH) $(call FixPath,$@)

.PRECIOUS: %/.d tmp/%.html

$(shell python ./pydeps -M > Makefile.pydeps)
include Makefile.pydeps

%.ly: %.genshi.ly
	python ./genshify -o $@ $< ${genshify_args}

out/guitar-fretboard.svg: guitar_layout.py sticker-def.genshi.xml guitar-base.genshi.xml guitar-strings.genshi.xml

out/piano-keyboard.svg: piano_layout.py

out/%.svg: %.genshi.svg $(OUT)
	python ./genshify -o $@ $< ${genshify_args}

out/%.png: out/%.svg
	inkscape $< -o $@

out/%.html: %.genshi.html $(html_includes) $(OUT)
	python ./genshify -o $@ $< ${genshify_args}

out/%.txt: %.genshi.txt $(OUT)
	python ./genshify -o $@ $< ${genshify_args}

# Remove temporary files to ensure regeneration of lilypond pictures, since lilypond-book does its own incomplete dependency check
out/%.html: tmp/%.html $(OUT) $(TMP)
	$(call ConditionalRmDir,out/lily/)
	$(LILYPOND_BOOK) --lily-output-dir out/lily/ --process "lilypond -dbackend=eps" --output out/ $<
	$(call ConditionalRmDir,out/lily/)

tmp/%.html: %.lilypond-genshi.html chromaturn.ly $(TMP)
	python ./genshify -o $@ $< ${genshify_args}

# We ensure that this is copied to the target directory, and actually compile from there
out/samples/%.ly: samples/%.ly $(SAMPLES)
	$(CP) $(call FixPath,$<) $(call FixPath,$@)

out/samples/%.pdf: out/samples/%.ly $(SAMPLES) chromaturn.ly
	lilypond --pdf -o $(@:.pdf=) $<

local: build_all
	$(MKDIR) ~/frasergo-website/frasergo-mezzanine/static/projects/harmonihue/
	rsync -avzP out/ ~/frasergo-website/frasergo-mezzanine/static/projects/harmonihue/

upload: build_all
	ssh longlake.frasergo.org "mkdir -p .virtualenv/frasergo/project/static/projects/harmonihue/"
	rsync -avzP out/ longlake.frasergo.org:.virtualenv/frasergo/project/static/projects/harmonihue/

