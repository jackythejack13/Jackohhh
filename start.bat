py startup.py
if %errorlevel% neq 0 exit /b %errorlevel%
ping 127.0.0.1 -n 6 > nul
py run.py
if %errorlevel% neq 0 echo "FATAL ERROR STATUS CODE %errorlevel%"
