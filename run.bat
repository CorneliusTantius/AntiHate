mode con: cols=75 lines=10
@echo off
cd bin
python --version >nul 2>&1 &&(
	echo "Collecting Requirements!"
	python -m pip install --upgrade pip
	pip install torch==1.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html /f >nul 2>&1
	pip install -r requirements.txt /f >nul 2>&1
	mode con: cols=40 lines=5
	echo "AntiHate is up and running"
	python main.py /f >nul 2>&1
) || (
	echo "Requirements not satisfied, please run inst-req.bat !!"
	pause
)