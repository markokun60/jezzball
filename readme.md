Setup
============
Create env
	py     -m venv .venv
	Visual Studio Code
		Cmd+shift+p
			Create enviroment
			

activate env
	windows
		.venv\Scripts\Activate.bat
	mac
		source .env/bin/activate

install
pip install pygame-ce
pip install pyinstaller

#pip install pygbag


create exe
--------------
Windows
pyinstaller --name pyJezzball  --onefile -w --icon=assets/jezzball.ico --add-data "assets:assets" --add-data "src/resources:resources"  src/main.py  
Mac
pyinstaller --name pyJezzball  --onefile -w --icon=assets/jezzball.icns --add-data "assets:assets" --add-data "src/resources:resources"  src/main.py  



