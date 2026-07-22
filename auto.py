
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
        'docs',
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
├── docs/
│   └── index.html
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


def create_index_html(package_name):
    """Create docs/index.html - Project landing page"""
    title = package_name.replace('_', ' ').title()
    
    content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Flutter Windows App</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .container {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 60px 50px;
            text-align: center;
            transition: transform 0.3s ease;
        }}

        .container:hover {{
            transform: translateY(-5px);
        }}

        .logo {{
            margin-bottom: 30px;
        }}

        .logo-svg {{
            width: 120px;
            height: 120px;
        }}

        h1 {{
            font-size: 2.5rem;
            color: #1a1a2e;
            margin-bottom: 10px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        .subtitle {{
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 30px;
            font-weight: 400;
        }}

        .badge-container {{
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 35px;
            flex-wrap: wrap;
        }}

        .badge {{
            background: #f0f0f0;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: #555;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .badge .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }}

        .badge .dot.green {{
            background: #4caf50;
        }}

        .badge .dot.blue {{
            background: #667eea;
        }}

        .badge .dot.orange {{
            background: #ff9800;
        }}

        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 35px 0 40px;
            text-align: left;
        }}

        .feature-item {{
            background: #f8f9fa;
            padding: 20px 20px 20px 25px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }}

        .feature-item:hover {{
            background: #f0f1ff;
            transform: translateX(5px);
        }}

        .feature-item .icon {{
            font-size: 1.5rem;
            margin-bottom: 8px;
        }}

        .feature-item h3 {{
            font-size: 0.95rem;
            color: #1a1a2e;
            margin-bottom: 4px;
        }}

        .feature-item p {{
            font-size: 0.85rem;
            color: #666;
            line-height: 1.4;
        }}

        .button-group {{
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 10px;
        }}

        .btn {{
            padding: 14px 32px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }}

        .btn-primary {{
            background: #667eea;
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-primary:hover {{
            background: #5a6fd6;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }}

        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
        }}

        .btn-secondary:hover {{
            background: #e0e0e0;
            transform: translateY(-2px);
        }}

        .btn-github {{
            background: #24292e;
            color: white;
        }}

        .btn-github:hover {{
            background: #1a1e22;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(36, 41, 46, 0.4);
        }}

        .version-info {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
            font-size: 0.9rem;
            color: #999;
        }}

        .version-info strong {{
            color: #667eea;
        }}

        @media (max-width: 640px) {{
            .container {{
                padding: 40px 25px;
            }}

            h1 {{
                font-size: 2rem;
            }}

            .feature-grid {{
                grid-template-columns: 1fr;
            }}

            .button-group {{
                flex-direction: column;
                align-items: stretch;
            }}

            .btn {{
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg class="logo-svg" viewBox="0 0 256 318" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M128 318L0 190.8V63.6L128 190.8L256 63.6V190.8L128 318Z" fill="#667eea" opacity="0.9"/>
                <path d="M128 190.8L0 63.6L128 -63.6L256 63.6L128 190.8Z" fill="#764ba2" opacity="0.8"/>
                <path d="M128 127.2L0 0V63.6L128 190.8L256 63.6V0L128 127.2Z" fill="#667eea" opacity="0.6"/>
                <circle cx="128" cy="63.6" r="12" fill="white" opacity="0.9"/>
                <circle cx="128" cy="190.8" r="12" fill="white" opacity="0.9"/>
            </svg>
        </div>

        <h1>{title}</h1>
        <p class="subtitle">A modern Flutter Windows application with automated builds</p>

        <div class="badge-container">
            <span class="badge">
                <span class="dot green"></span>
                Flutter
            </span>
            <span class="badge">
                <span class="dot blue"></span>
                Windows 10/11
            </span>
            <span class="badge">
                <span class="dot orange"></span>
                v1.0.0
            </span>
            <span class="badge">
                ⚡ GitHub Actions
            </span>
        </div>

        <div class="feature-grid">
            <div class="feature-item">
                <div class="icon">📱</div>
                <h3>Flutter Framework</h3>
                <p>Built with Flutter stable channel for modern UI</p>
            </div>
            <div class="feature-item">
                <div class="icon">🖥️</div>
                <h3>Windows Native</h3>
                <p>Fully integrated Windows desktop application</p>
            </div>
            <div class="feature-item">
                <div class="icon">🚀</div>
                <h3>CI/CD Ready</h3>
                <p>Automated builds with GitHub Actions</p>
            </div>
            <div class="feature-item">
                <div class="icon">📦</div>
                <h3>Easy Releases</h3>
                <p>One-command releases with tags</p>
            </div>
        </div>

        <div class="button-group">
            <a href="#" class="btn btn-primary">
                ⬇️ Download Latest
            </a>
            <a href="#" class="btn btn-github">
                <svg height="20" viewBox="0 0 16 16" width="20" fill="currentColor">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                </svg>
                View on GitHub
            </a>
            <a href="#" class="btn btn-secondary">
                📖 Documentation
            </a>
        </div>

        <div class="version-info">
            <strong>{package_name}</strong> • Built with ❤️ using Flutter • 
            <span id="year">2026</span>
        </div>
    </div>

    <script>
        document.getElementById('year').textContent = new Date().getFullYear();
    </script>
</body>
</html>
'''

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created: docs/index.html")


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
        create_index_html(package_name)

        # Make setup.sh executable on Unix-like systems
        if os.name != 'nt':
            os.chmod('setup.sh', 0o755)

        print("\n" + "=" * 60)
        print(" All files created successfully!")
        print("=" * 60)
        print("\nProject Structure:")
        print("   |-- .github/workflows/")
        print("   |   `-- build-windows.yml")
        print("   |-- docs/")
        print("   |   `-- index.html    (project landing page)")
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
        print("   5. View the landing page:")
        print("      - Open docs/index.html in your browser")

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
