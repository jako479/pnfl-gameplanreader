@ECHO OFF
cd /d "%~dp0"

:: ===================================================================
:: Edit the paths below to match your setup, then double-click to run.
:: This reads a game plan (.pln) and writes the play list to a file.
:: ===================================================================

SET GAMEPLAN_FILE=C:\PATH\TO\GAMEPLAN.pln
SET OUTPUT_FILE=C:\PATH\TO\PLAYS.txt

pnfl read-gameplan "%GAMEPLAN_FILE%" --normal-out "%OUTPUT_FILE%"

pause
