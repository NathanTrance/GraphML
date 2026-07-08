@echo off
echo ========================================
echo  Compiling main.tex with pdflatex + bibtex
echo ========================================

echo.
echo [1/4] Running pdflatex (pass 1)...
pdflatex -interaction=nonstopmode main.tex
if %errorlevel% neq 0 (
    echo ERROR: pdflatex pass 1 failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [2/4] Running bibtex...
bibtex main
if %errorlevel% neq 0 (
    echo WARNING: bibtex failed (check references.bib)
)

echo.
echo [3/4] Running pdflatex (pass 2)...
pdflatex -interaction=nonstopmode main.tex
if %errorlevel% neq 0 (
    echo ERROR: pdflatex pass 2 failed!
    pause
    exit /b %errorlevel%
)

echo.
echo [4/4] Running pdflatex (pass 3)...
pdflatex -interaction=nonstopmode main.tex
if %errorlevel% neq 0 (
    echo ERROR: pdflatex pass 3 failed!
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo  Done! Output: main.pdf
echo ========================================
pause
