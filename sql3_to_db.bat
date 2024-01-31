@echo off

set scriptFolder=userManagementTool
set scriptName=sql3_to_db.py
set baseFolder=%userprofile%\OneDrive - Gemeente Noordoostpolder\Bestanden USD-BEDRIJFSBUREAU\ETL en RPA\Draaiend op VPC0005\
set condaEnv=H:\GWS4ALL\Prod\RPA\Envs\nop_Productie



cd "%baseFolder%%scriptFolder%"


For /f "tokens=2-4 delims=- " %%a in ('date /t') do (set mydate=%%c-%%b-%%a)

set HH=%TIME: =0%
set HH=%HH:~0,2%
set MI=%TIME:~3,2%
set SS=%TIME:~6,2%
set FF=%TIME:~9,2%

set log_file="%baseFolder%log_%scriptname%_%mydate%_%HH%%MI%%SS%.txt"
set exit_file="%baseFolder%exitcode_%scriptname%_%mydate%_%HH%%MI%%SS%.txt"
if NOT %condaEnv%=="" (call conda activate %condaEnv% )


cd %baseFolder%%scriptFolder%

python %scriptName%
