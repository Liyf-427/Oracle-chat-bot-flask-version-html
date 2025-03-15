@echo off
cd /d E:\proj2501  REM 进入你的 Python 项目目录

REM 激活 Conda 环境（如果你在虚拟环境中运行）
call C:\Users\dell\anaconda3\Scripts\activate.bat
call conda activate pythonProject311

REM 启动 Socket 服务器
start "Socket Server" cmd /k python server_s.py

REM 等待 3 秒，确保服务器启动
timeout /t 3

REM 启动 Socket 客户端
start "Socket Client" cmd /k python socket_cli.py

exit
