mode con: cols=75 lines=10
@echo off
python --version >nul 2>&1 &&(
	echo "> Python found, prepping requirements"
	timeout /t 4
	cd bin 
	echo "> Please wait, installing requirements will take some time"
	pip install -r requirements.txt /f >nul 2>&1
	echo "> Requirements prepped!"
) || (
	echo "> Python not found, installing"
	timeout /t 4
	cd bin
	pyt.exe /quiet InstallAllUsers=1 PrependPath=1
	echo "> Python installed, prepping requirements"
	timeout /t 4
	echo "> Please wait, installing requirements will take some time"
	pip install -r requirements.txt /f >nul 2>&1
	echo "> Requirements prepped!"
)
pause