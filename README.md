User Guide
GitHub: https://github.com/Erikazyx/mymicro
Operating system: Windows 10 64bit
B.1  Required software
Make sure you have installed:
1.	Python 3.6.9
2.	Apache 2.4
B.2  Required packages
Use command: 
pip install -r requirements.txt
B.3 Apache Configuration
1.	Download mod_WSGI 
at :https://www.lfd.uci.edu/~gohlke/Pythonlibs/#mod_WSGI
choose the version that matches the running environment
for example, in mod_WSGI‑4.6.7+ap24vc14‑cp36‑cp36m‑win_amd64.whl, vc14 means visual c++ 14, cp36 means Python 3.6, amd64 means 64bit.
2.	Install a new server use this command:
httpd.exe -k install -n "apache2.4"
3.	Use command:
pip install mod_WSGI‑4.6.7+ap24vc14‑cp36‑cp36m‑win_amd64.whl
when it installed successfully, run another command:
mod_WSGI-express module-config
it will return 3 line of file address, like following:
 
Figure B.1 WSGI file address
Copy this three lines and paste to httpd.conf
Add the following lines too:
WSGIPythonPath D:\your\directory\webservice\pure
WSGIScriptAlias / D:\your\directory\webservice\pure\pure\WSGI.py
<Directory D:\your\directory\webservice\pure\pure>
<Files WSGI.py>
Require all granted
</Files>
</Directory>
B.4 LAN configuration
Use command:
ipconfig
Get your ipv4 address, modify your httpd.conf file, like following:
Listen IP address:port
ServerName address:port
Open windows firewall and add an inbound rule, choose TCP port type and enter the port which you just set in http.conf
B.5 Device configuration
1.compile the micro-manager API ,see: https://github.com/zfphil/micro-manager-python3
2.Find your devices on this web site: https://Micro-Manager.org/wiki/Device_Support
Open snap.py, in the function named initial(), change the demo device(like 'Cam', 'DemoCamera', 'DCam') to your own device. 
Open settings.py, modify ALLOWED_HOSTS = ['YOUR IP ADDRESS',’SERVERNAME’]
B.6 Runserver
On command line, at the directory of this ptoject,
Use command:
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000(*change to the port you like)

Run httpd server

Open browser, enter your IP address:prot