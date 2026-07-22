#!/usr/bin/env python3
"""
Auto-generate Flutter Windows App with GitHub Actions
Run: python create.py
"""

import os
import sys
import re
from pathlib import Path


def get_valid_package_name():
    """Get a valid Dart package name from user or generate one"""
    print("\nPackage Name Configuration")
    print("Rules: lowercase, underscore_separated, a-z0-9_")
    print("Example: my_app, simple_flutter_app, nova_client")
    print()

    # Try to get from directory name
    dir_name = os.path.basename(os.getcwd())
    # Convert to valid package name
    valid_name = re.sub(r'[^a-z0-9_]', '_', dir_name.lower())
    valid_name = re.sub(r'^[0-9_]+', '', valid_name)  # Remove leading numbers/underscores
    if not valid_name:
        valid_name = 'flutter_app'

    print(f"Suggested name from directory: {valid_name}")

    while True:
        name = input(f"Enter package name (or press Enter to use '{valid_name}'): ").strip()
        if not name:
            name = valid_name

        # Validate package name
        if re.match(r'^[a-z][a-z0-9_]*$', name):
            return name
        else:
            print("Invalid name! Use only lowercase letters, numbers, and underscores.")
            print("   Must start with a letter, no dashes or spaces.")
            print("   Example: my_app, simple_flutter_app\n")


def create_directory_structure():
    """Create all necessary directories"""
    dirs = [
        'lib',
        '.github/workflows',
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")


def create_main_dart():
    """Create lib/main.dart"""
    content = '''import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Simple Flutter App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Simple Flutter App'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.flutter_dash,
              size: 120,
              color: Colors.blue,
            ),
            const SizedBox(height: 20),
            const Text(
              'Hello, World!',
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              'Built with Flutter',
              style: TextStyle(
                fontSize: 20,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Button Clicked!'),
                    duration: Duration(seconds: 2),
                  ),
                );
              },
              icon: const Icon(Icons.thumb_up),
              label: const Text('Click Me'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 40,
                  vertical: 15,
                ),
                textStyle: const TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 30),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey.shade300),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  const Text(
                    'Version 1.0.0',
                    style: TextStyle(fontSize: 14, color: Colors.grey),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.desktop_windows, size: 16, color: Colors.grey.shade600),
                      const SizedBox(width: 5),
                      Text(
                        'Windows',
                        style: TextStyle(fontSize: 14, color: Colors.grey.shade600),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
'''

    with open('lib/main.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: lib/main.dart")


def create_pubspec(package_name):
    """Create pubspec.yaml with valid package name"""
    content = f'''name: {package_name}
description: A simple Flutter Windows application
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
'''

    with open('pubspec.yaml', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: pubspec.yaml (package: {package_name})")


def create_github_workflow(package_name):
    """Create .github/workflows/build-windows.yml"""
    content = '''name: Build and Release Windows App

on:
  push:
    branches: [ main, master ]
    tags:
      - 'v*'
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-2022

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        channel: 'stable'

    - name: Enable Windows desktop support
      run: flutter config --enable-windows-desktop

    - name: Create Windows project files
      run: flutter create --platforms=windows --project-name __PACKAGE_NAME__ .

    - name: Get dependencies
      run: flutter pub get

    - name: Build Windows app
      run: flutter build windows --release

    - name: List build output
      run: dir build\\windows\\x64\\runner\\Release

    - name: Upload build artifact
      uses: actions/upload-artifact@v4
      with:
        name: windows-app
        path: build/windows/x64/runner/Release/
        retention-days: 30

  create-release:
    needs: build-windows
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')

    steps:
    - name: Download Windows build
      uses: actions/download-artifact@v4
      with:
        name: windows-app
        path: windows-app

    - name: Zip the Windows app
      run: |
        cd windows-app
        zip -r ../simple-flutter-app-windows.zip .

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: simple-flutter-app-windows.zip
        name: Release ${{ github.ref_name }}
        draft: false
        prerelease: false
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''
    content = content.replace('__PACKAGE_NAME__', package_name)

    with open('.github/workflows/build-windows.yml', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: .github/workflows/build-windows.yml")


def create_gitignore():
    """Create .gitignore"""
    content = '''# Flutter
.dart_tool/
.packages/
build/
pubspec.lock
*.iml
*.iws
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Windows
*.exe
*.dll
*.pdb
*.ilk
*.exp
*.lib
*.suo
*.user
*.userosscache
*.sln.docstates

# Flutter Windows specific
windows/flutter/ephemeral/
windows/runner/Release/
'''

    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: .gitignore")


def create_setup_script(package_name):
    """Create setup.bat for Windows"""
    content = f'''@echo off
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
flutter create --platforms=windows --project-name {package_name} .

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
echo Output: build\\windows\\x64\\runner\\Release\\
echo.
pause
'''

    with open('setup.bat', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: setup.bat")


def create_setup_sh(package_name):
    """Create setup.sh for Linux/Mac"""
    content = f'''#!/bin/bash
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
flutter create --platforms=windows --project-name {package_name} .

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
'''

    with open('setup.sh', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: setup.sh")


def create_analysis_options():
    """Create analysis_options.yaml"""
    content = '''include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_final_fields: true
    use_key_in_widget_constructors: true
    avoid_print: true
    prefer_single_quotes: true
    avoid_void_async: true
    cancel_subscriptions: true
    close_sinks: true
    empty_statements: true
    hash_and_equals: true
    iterable_contains_unrelated_type: true
    list_remove_unrelated_type: true
    no_adjacent_strings_in_list: true
    no_duplicate_case_values: true
    unrelated_type_equality_checks: true
    use_full_hex_values_for_flutter_colors: true
'''

    with open('analysis_options.yaml', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: analysis_options.yaml")


def create_readme(package_name):
    """Create README.md"""
    content = f'''# {package_name.replace('_', ' ').title()}

A simple Flutter Windows application with automated GitHub Actions builds.

## Features

- Built with Flutter (stable channel)
- Windows desktop support
- Automated builds with GitHub Actions
- Release artifacts automatically attached to releases

## Development

### Prerequisites

- Flutter SDK (stable channel)
- Windows 10/11
- Visual Studio 2022 with C++ development tools

### Run Locally

```bash
# Get dependencies
flutter pub get

# Create Windows files (first time only)
flutter create --platforms=windows --project-name {package_name} .

# Run the app
flutter run

# Build for Windows
flutter build windows --release
```

## GitHub Actions

The workflow automatically:
1. Builds the Windows app on every push
2. Uploads the build as an artifact
3. Creates a release when you push a tag

### Create a Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── build-windows.yml
├── lib/
│   └── main.dart
├── windows/         # Created by flutter create
├── analysis_options.yaml
├── pubspec.yaml
├── .gitignore
├── setup.bat  (Windows)
└── setup.sh   (Linux/Mac)
```

## Build Output

The Windows build is located at:
```
build/windows/x64/runner/Release/
```

## Troubleshooting

### "No Windows desktop project configured"
Run: `flutter create --platforms=windows --project-name {package_name} .`

### "Invalid package name" (referring to the checkout/folder name, not pubspec.yaml)
`flutter create .` derives the project name from the current directory name
unless you pass `--project-name` explicitly. If your repo/folder name contains
dashes (e.g. `my-repo`), always pass `--project-name` (as this workflow and
setup scripts already do) instead of relying on the folder name.

### CMake "could not find any instance of Visual Studio"
Make sure the workflow pins `runs-on: windows-2022` (not `windows-latest`)
and does not pin an old Flutter version that predates the Visual Studio
release on the runner.

## License

MIT
'''

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: README.md")


def main():
    """Main function to create all files"""
    print("\n" + "=" * 60)
    print(" Flutter Windows App Generator")
    print("=" * 60 + "\n")

    # Check if Flutter project already exists
    if os.path.exists('lib') or os.path.exists('pubspec.yaml'):
        response = input("This directory already has Flutter files. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)

    try:
        # Get valid package name
        package_name = get_valid_package_name()

        print("\n" + "=" * 60)
        print(f" Creating project: {package_name}")
        print("=" * 60 + "\n")

        # Create all files
        create_directory_structure()
        print()
        create_main_dart()
        create_pubspec(package_name)
        create_github_workflow(package_name)
        create_gitignore()
        create_setup_script(package_name)
        create_setup_sh(package_name)
        create_analysis_options()
        create_readme(package_name)

        # Make setup.sh executable on Unix-like systems
        if os.name != 'nt':
            os.chmod('setup.sh', 0o755)

        print("\n" + "=" * 60)
        print(" All files created successfully!")
        print("=" * 60)
        print("\nProject Structure:")
        print("   |-- .github/workflows/")
        print("   |   `-- build-windows.yml")
        print("   |-- lib/")
        print("   |   `-- main.dart")
        print("   |-- windows/         (will be created by flutter create)")
        print("   |-- analysis_options.yaml")
        print("   |-- pubspec.yaml")
        print("   |-- README.md")
        print("   |-- .gitignore")
        print("   |-- setup.bat  (Windows)")
        print("   `-- setup.sh   (Linux/Mac)")

        print(f"\nPackage Name: {package_name}")

        print("\nNext Steps:")
        print("   1. Run setup script:")
        print("      - Windows: setup.bat")
        print("      - Linux/Mac: ./setup.sh")
        print("   2. Or manually:")
        print("      - flutter pub get")
        print(f"      - flutter create --platforms=windows --project-name {package_name} .")
        print("      - flutter build windows --release")
        print("   3. Initialize Git:")
        print("      - git init")
        print("      - git add .")
        print("      - git commit -m 'Initial commit'")
        print("   4. Push to GitHub and Actions will build automatically")

        print("\nTo create a release:")
        print("   git tag v1.0.0")
        print("   git push origin v1.0.0")

        print("\n" + "=" * 60)

    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()