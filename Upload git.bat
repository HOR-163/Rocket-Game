@echo off
git init
git add .
set /p message="Enter your commit message:"
git commit -m %message%
git branch -M main
git remote add origin https://github.com/HOR-163/Rocket-Game.git
git push -u origin main
echo \033[32mDone!
pause