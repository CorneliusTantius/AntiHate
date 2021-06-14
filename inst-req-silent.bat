mode con: cols=75 lines=10
@echo off
python --version >nul 2>&1 &&(
	echo "> Python found, prepping requirements"
	timeout /t 4
	cd bin 
	python -m pip install --upgrade pip
	echo "> Please wait, installing requirements will take some time"
	pip install torch==1.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html /f >nul 2>&1
	pip install -r requirements.txt /f >nul 2>&1
	echo "> Requirements prepped!"
) || (
	echo "> Python not found, installing"
	timeout /t 4
	cd bin
	pyt64.exe /quiet InstallAllUsers=1 PrependPath=1
	echo "> Python installed, prepping requirements"
	timeout /t 4
	python -m pip install --upgrade pip
	echo "> Please wait, installing requirements will take some time"
	pip install torch==1.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html /f >nul 2>&1
	pip install -r requirements.txt /f >nul 2>&1
	echo "> Requirements prepped!"
)
pause