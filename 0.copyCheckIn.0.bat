cd /d "%~dp0"  

set server=10.1.9.189
rem %server%  

set dataFileFrom="\\%server%\c$\Program Files (x86)\ZKTime5.0\"
set dataJsonFrom="\\%server%\c$\SZ_Check_In\"
set dataFileName=att2000.mdb

set dataFileTo=check-in-data\

rmdir /S /Q %cd%\%dataFileTo%  

net use /delete \\%server%\c$ /Y  

net use \\%server%\c$ 123 /user:administrator  

echo %dataFileFrom%%dataFileName% %dataFileTo% 

xcopy %dataFileFrom%%dataFileName% %dataFileTo% 
xcopy %dataJsonFrom%leave.json %dataFileTo% 
xcopy %dataJsonFrom%persons.json %dataFileTo% 

python2 check-in-py\check-in.py

::pause & exit