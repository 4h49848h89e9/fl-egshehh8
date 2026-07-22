#!/usr/bin/env python3
"""
fully.py - OryvexVPN Flutter Windows Generator
Creates all Dart files, assets, and native plugin stub.
Does NOT require Flutter to be installed.
"""

import os
import sys
import shutil
from pathlib import Path

# ===== CONFIGURATION =====
PROJECT_ROOT = Path(__file__).parent.resolve()
CS_PROJECT_ROOT = Path(r"C:\Users\nasle javan\Desktop\OryvexVPNCore")
CS_CORE_DIR = CS_PROJECT_ROOT / "OryvexVPN" / "Core"
CS_FONTS_DIR = CS_PROJECT_ROOT / "OryvexVPN" / "Fonts"

ASSETS_TO_COPY = {
    "config": CS_CORE_DIR / "oryvexvpn-config.json",
    "xray": CS_CORE_DIR / "xray.exe",
    "wintun": CS_CORE_DIR / "wintun.dll",
    "geoip": CS_CORE_DIR / "geoip.dat",
    "geosite": CS_CORE_DIR / "geosite.dat",
    "icon": CS_PROJECT_ROOT / "OryvexVPN" / "icon.ico",
    "logo": CS_PROJECT_ROOT / "OryvexVPN" / "logo.png",
    "fonts_bold": CS_FONTS_DIR / "Inter-Bold.ttf",
    "fonts_medium": CS_FONTS_DIR / "Inter-Medium.ttf",
    "fonts_regular": CS_FONTS_DIR / "Inter-Regular.ttf",
}

def print_header(text: str) -> None:
    print(f"\n{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}\n")

def print_success(text: str) -> None:
    print(f"✅ {text}")

def print_error(text: str) -> None:
    print(f"❌ {text}")

def print_info(text: str) -> None:
    print(f"ℹ️  {text}")

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def copy_file(src: Path, dst: Path) -> bool:
    if not src.exists():
        print_error(f"Source not found: {src}")
        return False
    ensure_dir(dst.parent)
    try:
        shutil.copy2(src, dst)
        print_success(f"Copied {src.name} -> {dst}")
        return True
    except Exception as e:
        print_error(f"Copy failed: {e}")
        return False

def write_file(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding='utf-8')
    print_success(f"Created {path}")

def main() -> None:
    print_header("ORYEXVPN FLUTTER BUILDER (fully.py)")

    # 1. Clean old lib/ and assets/
    print_info("Deleting old lib/ and assets/ ...")
    for d in [PROJECT_ROOT / "lib", PROJECT_ROOT / "assets"]:
        if d.exists():
            shutil.rmtree(d)
            print_success(f"Deleted {d.name}/")

    # 2. Create asset directories
    asset_dirs = [
        PROJECT_ROOT / "assets" / "config",
        PROJECT_ROOT / "assets" / "core",
        PROJECT_ROOT / "assets" / "fonts",
        PROJECT_ROOT / "assets" / "images",
    ]
    for d in asset_dirs:
        ensure_dir(d)
        print_success(f"Created {d}")

    # 3. Copy assets from C# project
    print_info("Copying assets from OryvexVPNCore...")
    copy_file(ASSETS_TO_COPY["config"], PROJECT_ROOT / "assets" / "config" / "oryvexvpn-config.json")
    copy_file(ASSETS_TO_COPY["xray"], PROJECT_ROOT / "assets" / "core" / "xray.exe")
    copy_file(ASSETS_TO_COPY["wintun"], PROJECT_ROOT / "assets" / "core" / "wintun.dll")
    copy_file(ASSETS_TO_COPY["geoip"], PROJECT_ROOT / "assets" / "core" / "geoip.dat")
    copy_file(ASSETS_TO_COPY["geosite"], PROJECT_ROOT / "assets" / "core" / "geosite.dat")
    copy_file(ASSETS_TO_COPY["icon"], PROJECT_ROOT / "assets" / "images" / "icon.ico")
    copy_file(ASSETS_TO_COPY["logo"], PROJECT_ROOT / "assets" / "images" / "logo.png")
    copy_file(ASSETS_TO_COPY["fonts_bold"], PROJECT_ROOT / "assets" / "fonts" / "Inter-Bold.ttf")
    copy_file(ASSETS_TO_COPY["fonts_medium"], PROJECT_ROOT / "assets" / "fonts" / "Inter-Medium.ttf")
    copy_file(ASSETS_TO_COPY["fonts_regular"], PROJECT_ROOT / "assets" / "fonts" / "Inter-Regular.ttf")

    # 4. Generate Dart source files
    print_info("Generating Dart source files...")

    # ---- lib/main.dart ----
    write_file(PROJECT_ROOT / "lib" / "main.dart", """
import 'package:flutter/material.dart';
import 'package:simpleflutter/views/home_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OryvexVPN',
      theme: ThemeData.dark().copyWith(
        primaryColor: Colors.blue,
        colorScheme: const ColorScheme.dark(primary: Colors.blue),
        scaffoldBackgroundColor: const Color(0xFF0A0A0A),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0D0D0D),
          elevation: 0,
        ),
      ),
      home: const HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}
""")

    # ---- lib/views/home_page.dart ----
    write_file(PROJECT_ROOT / "lib" / "views" / "home_page.dart", """
import 'package:flutter/material.dart';
import 'package:simpleflutter/widgets/sidebar.dart';
import 'package:simpleflutter/views/dashboard_view.dart';
import 'package:simpleflutter/views/settings_view.dart';
import 'package:simpleflutter/views/logs_view.dart';
import 'package:simpleflutter/views/config_view.dart';
import 'package:simpleflutter/views/diagnostics_view.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  final List<Widget> _views = const [
    DashboardView(),
    SettingsView(),
    LogsView(),
    ConfigView(),
    DiagnosticsView(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Sidebar(
            selectedIndex: _selectedIndex,
            onItemSelected: (index) {
              setState(() {
                _selectedIndex = index;
              });
            },
          ),
          Expanded(
            child: _views[_selectedIndex],
          ),
        ],
      ),
    );
  }
}
""")

    # ---- lib/widgets/sidebar.dart ----
    write_file(PROJECT_ROOT / "lib" / "widgets" / "sidebar.dart", """
import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  final int selectedIndex;
  final ValueChanged<int> onItemSelected;

  const Sidebar({
    super.key,
    required this.selectedIndex,
    required this.onItemSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 80,
      color: const Color(0xFF0A0A0A),
      child: Column(
        children: [
          const SizedBox(height: 28),
          Image.asset('assets/images/logo.png', width: 40, height: 40),
          const Spacer(),
          _buildNavItem(Icons.dashboard, 0, 'Dashboard'),
          _buildNavItem(Icons.settings, 1, 'Settings'),
          _buildNavItem(Icons.terminal, 2, 'Logs'),
          _buildNavItem(Icons.code, 3, 'Config'),
          _buildNavItem(Icons.health_and_safety, 4, 'Diagnostics'),
          const Spacer(),
          IconButton(
            icon: const Icon(Icons.send, color: Colors.grey),
            onPressed: () {},
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildNavItem(IconData icon, int index, String tooltip) {
    final isSelected = selectedIndex == index;
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 6),
      decoration: BoxDecoration(
        color: isSelected ? const Color(0xFF1E2A3A) : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
      ),
      child: IconButton(
        icon: Icon(icon, color: isSelected ? Colors.blue : Colors.grey[600]),
        onPressed: () => onItemSelected(index),
        tooltip: tooltip,
      ),
    );
  }
}
""")

    # ---- lib/views/dashboard_view.dart ----
    write_file(PROJECT_ROOT / "lib" / "views" / "dashboard_view.dart", """
import 'package:flutter/material.dart';
import 'package:simpleflutter/services/vpn_service.dart';
import 'package:simpleflutter/widgets/connection_button.dart';
import 'package:simpleflutter/widgets/stats_card.dart';

class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  State<DashboardView> createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  final VpnService _vpnService = VpnService();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Column(
        children: [
          const Text(
            'PROTECTION SECURED',
            style: TextStyle(
              color: Colors.blue,
              fontSize: 24,
              fontWeight: FontWeight.bold,
              letterSpacing: 2,
            ),
          ),
          const SizedBox(height: 30),
          ConnectionButton(
            isConnected: _vpnService.isConnected,
            isConnecting: _vpnService.isConnecting,
            onPressed: _vpnService.toggleConnection,
          ),
          const SizedBox(height: 40),
          Row(
            children: const [
              Expanded(child: StatsCard(icon: Icons.speed, label: 'LATENCY', value: '42 ms')),
              Expanded(child: StatsCard(icon: Icons.arrow_downward, label: 'DOWNLOAD', value: '0 B/s')),
              Expanded(child: StatsCard(icon: Icons.arrow_upward, label: 'UPLOAD', value: '0 B/s')),
            ],
          ),
        ],
      ),
    );
  }
}
""")

    # ---- lib/views/settings_view.dart ----
    write_file(PROJECT_ROOT / "lib" / "views" / "settings_view.dart", """
import 'package:flutter/material.dart';

class SettingsView extends StatelessWidget {
  const SettingsView({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Settings View - Coming soon', style: TextStyle(color: Colors.grey)),
    );
  }
}
""")

    # ---- lib/views/logs_view.dart ----
    write_file(PROJECT_ROOT / "lib" / "views" / "logs_view.dart", """
import 'package:flutter/material.dart';

class LogsView extends StatelessWidget {
  const LogsView({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('System Logs - Coming soon', style: TextStyle(color: Colors.grey)),
    );
  }
}
""")

    # ---- lib/views/config_view.dart ----
    write_file(PROJECT_ROOT / "lib" / "views" / "config_view.dart", """
import 'package:flutter/material.dart';

class ConfigView extends StatelessWidget {
  const ConfigView({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Advanced Config - Coming soon', style: TextStyle(color: Colors.grey)),
    );
  }
}
""")

    # ---- lib/views/diagnostics_view.dart ----
    write_file(PROJECT_ROOT / "lib" / "views" / "diagnostics_view.dart", """
import 'package:flutter/material.dart';

class DiagnosticsView extends StatelessWidget {
  const DiagnosticsView({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('Diagnostics - Coming soon', style: TextStyle(color: Colors.grey)),
    );
  }
}
""")

    # ---- lib/widgets/connection_button.dart ----
    write_file(PROJECT_ROOT / "lib" / "widgets" / "connection_button.dart", """
import 'package:flutter/material.dart';

class ConnectionButton extends StatelessWidget {
  final bool isConnected;
  final bool isConnecting;
  final VoidCallback onPressed;

  const ConnectionButton({
    super.key,
    required this.isConnected,
    required this.isConnecting,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: isConnecting ? null : onPressed,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        width: 170,
        height: 170,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: isConnected ? Colors.blue : (isConnecting ? Colors.grey[800] : Colors.grey[900]),
          boxShadow: isConnected
              ? [BoxShadow(color: Colors.blue.withOpacity(0.5), blurRadius: 20, spreadRadius: 5)]
              : [],
        ),
        child: Icon(
          isConnected ? Icons.shield : (isConnecting ? Icons.wifi : Icons.power_settings_new),
          size: 76,
          color: Colors.white,
        ),
      ),
    );
  }
}
""")

    # ---- lib/widgets/stats_card.dart ----
    write_file(PROJECT_ROOT / "lib" / "widgets" / "stats_card.dart", """
import 'package:flutter/material.dart';

class StatsCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const StatsCard({
    super.key,
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF0D0D0D),
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: Colors.blue, size: 26),
            const SizedBox(height: 16),
            Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
""")

    # ---- lib/services/vpn_service.dart ----
    write_file(PROJECT_ROOT / "lib" / "services" / "vpn_service.dart", """
import 'package:flutter/services.dart';

class VpnService {
  static const MethodChannel _channel = MethodChannel('com.oryvexvpn/vpn');

  bool _isConnected = false;
  bool _isConnecting = false;

  bool get isConnected => _isConnected;
  bool get isConnecting => _isConnecting;

  Future<void> toggleConnection() async {
    if (_isConnecting) return;
    _isConnecting = true;
    try {
      if (_isConnected) {
        await _channel.invokeMethod('disconnect');
        _isConnected = false;
      } else {
        await _channel.invokeMethod('connect');
        _isConnected = true;
      }
    } catch (e) {
      // handle error
    } finally {
      _isConnecting = false;
    }
  }
}
""")

    # 5. Generate pubspec.yaml
    write_file(PROJECT_ROOT / "pubspec.yaml", """
name: simpleflutter
description: OryvexVPN - Flutter Windows Client
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  url_launcher: ^6.2.1
  path_provider: ^2.1.0
  process_run: ^0.13.0
  win32: ^5.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true

  assets:
    - assets/config/
    - assets/core/
    - assets/images/
    - assets/fonts/

  fonts:
    - family: Inter
      fonts:
        - asset: assets/fonts/Inter-Regular.ttf
        - asset: assets/fonts/Inter-Medium.ttf
          weight: 500
        - asset: assets/fonts/Inter-Bold.ttf
          weight: 700
""")

    # 6. Generate Windows native plugin stub
    print_info("Generating Windows plugin stub...")
    windows_plugin_dir = PROJECT_ROOT / "windows" / "plugins" / "vpn_plugin"
    ensure_dir(windows_plugin_dir)

    write_file(windows_plugin_dir / "vpn_plugin.cpp", """
#include <flutter/method_channel.h>
#include <flutter/plugin_registrar_windows.h>
#include <windows.h>

using namespace flutter;

class VpnPlugin {
public:
    static void RegisterWithRegistrar(PluginRegistrarWindows* registrar) {
        auto channel = std::make_unique<MethodChannel<>>(
            registrar->messenger(), "com.oryvexvpn/vpn",
            &StandardMethodCodec::GetInstance());
        auto* channel_raw = channel.get();
        registrar->AddPlugin(std::move(channel));
        channel_raw->SetMethodCallHandler([](const MethodCall<>& call,
                                             std::unique_ptr<MethodResult<>> result) {
            if (call.method_name() == "connect") {
                // TODO: Start Xray/Aether processes
                // For now just return success
                result->Success();
            } else if (call.method_name() == "disconnect") {
                // TODO: Stop processes
                result->Success();
            } else {
                result->NotImplemented();
            }
        });
    }
};

extern "C" __declspec(dllexport) void RegisterPlugins(
    PluginRegistrarWindows* registrar) {
    VpnPlugin::RegisterWithRegistrar(registrar);
}
""")

    # Also generate a CMakeLists.txt for the plugin (to be included manually)
    write_file(windows_plugin_dir / "CMakeLists.txt", """
cmake_minimum_required(VERSION 3.15)
project(vpn_plugin)

add_library(vpn_plugin SHARED vpn_plugin.cpp)
target_include_directories(vpn_plugin PRIVATE ${FLUTTER_ENGINE_DIR}/include)
target_link_libraries(vpn_plugin PRIVATE flutter_engine)
""")

    # 7. Generate a README with instructions for native integration
    write_file(PROJECT_ROOT / "WINDOWS_PLUGIN_README.md", """
# Native Windows Plugin Integration

The VPN functionality requires a native plugin to:
- Spawn xray.exe (or aether.exe)
- Set/clear system proxy via Windows Registry
- Generate and trust Root CA certificate

We have provided a stub plugin in `windows/plugins/vpn_plugin/`.

## To integrate:
1. Copy the plugin folder into your Windows runner after `flutter create`.
2. Add the plugin to the main CMakeLists.txt by including the subdirectory and linking.

The GitHub Actions workflow will run `flutter create`, so you may need to copy these files into the generated `windows/` folder after creation. Consider modifying your workflow to copy these files after the `flutter create` step.

Alternatively, you can generate the full Windows project locally once and commit it (removing the `flutter create` step from the workflow).
""")

    print_header("✅ GENERATION COMPLETE")
    print("All Dart source files and assets have been created.")
    print("The native plugin stub is in windows/plugins/vpn_plugin/")
    print("See WINDOWS_PLUGIN_README.md for integration instructions.")
    print("Now you can commit and push to GitHub.")
    print("The existing workflow will build the app (it runs `flutter create` and then builds).")
    print(f"Project location: {PROJECT_ROOT}")

if __name__ == "__main__":
    main()