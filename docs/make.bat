@echo off
REM Build documentation (Windows)
if "%1"=="" goto usage

if "%1"=="html" (
    sphinx-build -b html . _build\html
    goto end
)

if "%1"=="latexpdf" (
    sphinx-build -b latex . _build\latex
    REM Attempt to run pdflatex on generated .tex file
    for %%f in (_build\latex\*.tex) do (
        pdflatex -interaction=nonstopmode -halt-on-error -output-directory=_build\latex %%f
        pdflatex -interaction=nonstopmode -halt-on-error -output-directory=_build\latex %%f
    )
    goto end
)

:usage
echo Usage: make.bat ^(html^|latexpdf^)

:end
