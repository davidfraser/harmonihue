@echo off
if EXIST %LILYPOND_HOME%\usr\bin\convert-ly.py (
    set CONVERT_LY=python %LILYPOND_HOME%\usr\bin\convert-ly.py
) else if EXIST %LILYPOND_HOME%\usr\bin\convert-ly (
    set CONVERT_LY=python %LILYPOND_HOME%\usr\bin\convert-ly
) else (
    echo Could not find convert-ly >&2
    exit /b 1
)
for %%F in (*.ly) do (%CONVERT_LY% %* %%F > %%F.converted && move /Y %%F.converted %%F)
