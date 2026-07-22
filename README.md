# Simpleflutter

A simple Flutter Windows application with automated GitHub Actions builds.

## Features

- 🚀 Built with Flutter 3.24.0
- 🪟 Windows desktop support
- 🤖 Automated builds with GitHub Actions
- 📦 Release artifacts automatically attached to releases

## Development

### Prerequisites

- Flutter SDK 3.24.0+
- Windows 10/11
- Visual Studio 2022 with C++ development tools

### Run Locally

```bash
# Get dependencies
flutter pub get

# Create Windows files (first time only)
flutter create --platforms=windows .

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
Run: `flutter create --platforms=windows .`

### Invalid package name
Make sure your package name in `pubspec.yaml` is:
- All lowercase
- Uses underscores (not dashes)
- Starts with a letter
- Example: `my_app`, `simple_flutter_app`

## License

MIT
