@echo off
:loop
git checkout %1%_dev
git merge master
git push
git checkout master
shift
if not "%~1"=="" goto loop