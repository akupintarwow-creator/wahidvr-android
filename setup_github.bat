@echo off
echo ========================================
echo  WahidVR Kamera - Setup GitHub Actions
echo ========================================
echo.

echo [1/4] Inisialisasi Git...
git init
git add .
git commit -m "Initial commit: WahidVR Kamera Android"

echo.
echo [2/4] Repository baru akan dibuat di GitHub...
echo Buka: https://github.com/new
echo Buat repository baru dengan nama: wahidvr-android
echo.
pause

echo.
echo [3/4] Masukkan URL repository GitHub kamu:
set /p REPO_URL="URL (contoh: https://github.com/username/wahidvr-android.git): "

echo.
echo [4/4] Push ke GitHub...
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  Selesai! GitHub Actions akan auto-build
echo  APK dalam beberapa menit.
echo.
echo  Cek: https://github.com/username/wahidvr-android/actions
echo  Download APK di: Actions > Build > Artifacts
echo ========================================
pause
