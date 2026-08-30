@echo off
rmdir /s /q report\allure-results
pytest tugas_5.py --alluredir=report/allure-results
allure generate --single-file report/allure-results --name login-test --clean -o report/allure-report
pause