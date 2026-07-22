@echo off
echo ====================================
echo  Flutter Windows App Setup
echo ====================================
echo.

echo Checking Flutter installation...
flutter --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Flutter not found. Please install Flutter.
    echo https://flutter.dev/docs/get-started/install/windows
    pause
    exit /b 1
)

echo.
echo Enabling Windows desktop support...
flutter config --enable-windows-desktop

echo.
echo Creating Windows project files...
flutter create --platforms=windows --project-name simpleflutter .

echo.
echo Getting dependencies...
flutter pub get

echo.
echo Building Windows app...
flutter build windows --release

echo.
echo ====================================
echo  Build Complete!
echo ====================================
echo.
echo Output: build\windows\x64\runner\Release\
echo.
pause
