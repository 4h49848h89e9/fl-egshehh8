#!/bin/bash
# Setup script for Flutter Windows app

echo "===================================="
echo " Flutter Windows App Setup"
echo "===================================="
echo ""

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "[ERROR] Flutter not found. Please install Flutter."
    echo "https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "Enabling Windows desktop support..."
flutter config --enable-windows-desktop

echo ""
echo "Creating Windows project files..."
flutter create --platforms=windows .

echo ""
echo "Getting dependencies..."
flutter pub get

echo ""
echo "Building Windows app..."
flutter build windows --release

echo ""
echo "===================================="
echo " Build Complete!"
echo "===================================="
echo ""
echo "Output: build/windows/x64/runner/Release/"
echo ""
