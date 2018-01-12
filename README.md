
# SZ-Check-In
For reminder seeker to check in.

1. jenkins run on slave(50) at every morning 10:00;
2. jenkins trigger 0.copyCheckIn.bat
3. 0.copyCheckIn.bat - copy files from OA server(10.1.9.189): att2000.mdb + persons.json + leave.json; trigger check-in.py
    * att2000.mdb  - DB for OA
    * persons.json - Staff info
    * leave.json   - holiday, workday at weekend，personal holiday
4. check-in-py/check-in.py  - check staff that not check in, then send mail and slack
5. check-in-py/sendmail.py  - send mail to staff
6. check-in-py/sendslack.py - send notification to slack