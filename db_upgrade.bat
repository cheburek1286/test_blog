set FLASK_APP=main.py

if NOT EXIST migrations flask db init

flask db upgrade

pause