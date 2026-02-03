@echo off
cd /d k:\blogger-html-automation

for %%F in (output\*) do (
    echo Moving %%~nxF to post folder...
    move "%%F" "post\%%~nxF"
    
    echo Committing %%~nxF...
    git add "post\%%~nxF"
    git commit -m "Add %%~nxF to post folder"
    
    echo.
)

echo All files committed!
pause