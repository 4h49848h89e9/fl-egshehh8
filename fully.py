#!/usr/bin/env python3
"""
fully.py - Ultimate OryvexVPN Flutter Generator & Pusher
Creates all files, copies assets, commits, and force-pushes with tagging.
No external Flutter needed.
"""

import os
import sys
import shutil
import re
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
#  CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).parent.resolve()
CS_PROJECT_ROOT = Path(r"C:\Users\nasle javan\Desktop\OryvexVPNCore")
CS_CORE_DIR = CS_PROJECT_ROOT / "OryvexVPN" / "Core"
CS_FONTS_DIR = CS_PROJECT_ROOT / "OryvexVPN" / "Fonts"

REPO_OWNER = "4h49848h89e9"
REPO_NAME = "fl-egshehh8"

# Files to copy from the C# project
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

GIT_TIMEOUT = 300  # seconds for push operations

# ============================================================
#  UTILITIES
# ============================================================
def print_header(text):
    print(f"\n{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)

def copy_file(src, dst):
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

def write_file(path, content):
    ensure_dir(path.parent)
    path.write_text(content, encoding='utf-8')
    print_success(f"Created {path}")

def run_git_command(cmd, timeout=GIT_TIMEOUT):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=str(PROJECT_ROOT), timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print_error(f"Git command timed out after {timeout}s: {cmd}")
        return None
    except Exception as e:
        print_error(f"Git command exception: {e}")
        return None

# ============================================================
#  GENERATE FLUTTER PROJECT FILES
# ============================================================
def generate_flutter_project():
    print_info("Deleting old lib/ and assets/ ...")
    for d in [PROJECT_ROOT / "lib", PROJECT_ROOT / "assets"]:
        if d.exists():
            shutil.rmtree(d)
            print_success(f"Deleted {d.name}/")

    # Asset directories
    asset_dirs = [
        PROJECT_ROOT / "assets" / "config",
        PROJECT_ROOT / "assets" / "core",
        PROJECT_ROOT / "assets" / "fonts",
        PROJECT_ROOT / "assets" / "images",
    ]
    for d in asset_dirs:
        ensure_dir(d)
        print_success(f"Created {d}")

    # Copy assets
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

    # ---- Generate Dart files ----
    print_info("Generating Dart source files...")

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

    # ---- pubspec.yaml ----
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

    # ---- Windows plugin stub ----
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

    write_file(windows_plugin_dir / "CMakeLists.txt", """
cmake_minimum_required(VERSION 3.15)
project(vpn_plugin)

add_library(vpn_plugin SHARED vpn_plugin.cpp)
target_include_directories(vpn_plugin PRIVATE ${FLUTTER_ENGINE_DIR}/include)
target_link_libraries(vpn_plugin PRIVATE flutter_engine)
""")

    print_success("All Flutter files generated.")

# ============================================================
#  GIT PUSH LOGIC (with extended timeout)
# ============================================================
def git_add_all():
    print_info("git add -A")
    result = run_git_command("git add -A")
    if result and result.returncode == 0:
        print_success("git add -A successful")
        return True
    print_error("git add -A failed")
    return False

def git_commit(message):
    print_info(f'git commit -m "{message}"')
    result = run_git_command(f'git commit -m "{message}"')
    if result and result.returncode == 0:
        print_success("Commit successful.")
        return True
    if result and "nothing to commit" in (result.stderr or ""):
        print_warning("No changes to commit.")
        return True
    print_error("Commit failed.")
    return False

def git_force_push():
    print_info("git push --force origin main (timeout: 300s)")
    result = run_git_command("git push --force origin main", timeout=300)
    if result and result.returncode == 0:
        print_success("Force push successful.")
        return True
    print_error("Force push failed.")
    return False

def get_next_version_tag():
    result = run_git_command("git tag -l", timeout=30)
    if result is None:
        return "v1.0.1"
    tags = result.stdout.splitlines()
    pattern = re.compile(r'^v(\d+)\.(\d+)\.(\d+)$')
    max_version = [1, 0, 0]
    for tag in tags:
        match = pattern.match(tag)
        if match:
            major, minor, patch = map(int, match.groups())
            if (major, minor, patch) > tuple(max_version):
                max_version = [major, minor, patch]
    max_version[2] += 1
    return f"v{max_version[0]}.{max_version[1]}.{max_version[2]}"

def delete_existing_tag(tag_name):
    print_info(f"Deleting existing tag: {tag_name}")
    run_git_command(f"git tag -d {tag_name}", timeout=30)
    run_git_command(f"git push origin :refs/tags/{tag_name}", timeout=60)

def create_and_push_tag(tag_name):
    print_info(f"Creating and pushing tag: {tag_name}")
    delete_existing_tag(tag_name)
    result = run_git_command(f"git tag {tag_name}", timeout=30)
    if result is None or result.returncode != 0:
        print_error("Tag creation failed.")
        return False
    result = run_git_command(f"git push origin {tag_name}", timeout=60)
    if result and result.returncode == 0:
        print_success(f"Tag {tag_name} pushed successfully.")
        return True
    print_error("Tag push failed.")
    return False

def check_git_config():
    name = run_git_command("git config --global user.name", timeout=10)
    email = run_git_command("git config --global user.email", timeout=10)
    if not name or not name.stdout.strip() or not email or not email.stdout.strip():
        print_info("Setting default git config...")
        run_git_command('git config --global user.name "Auto Pusher"', timeout=10)
        run_git_command('git config --global user.email "auto@pusher.local"', timeout=10)
    return True

def push_to_github():
    print_header("GIT PUSH")
    if not check_git_config():
        print_error("Git config check failed.")
        return False

    print_info("Adding all files...")
    if not git_add_all():
        return False

    commit_msg = f"Auto-fix: {datetime.now().strftime('%Y-%m-%d %H:%M')} (fully.py)"
    print_info("Committing...")
    if not git_commit(commit_msg):
        print_warning("Trying empty commit...")
        result = run_git_command('git commit --allow-empty -m "Auto-fix: No changes"', timeout=30)
        if result and result.returncode != 0:
            print_error("Commit failed. Aborting push.")
            return False

    print_info("Force pushing...")
    if not git_force_push():
        return False

    new_tag = get_next_version_tag()
    print_info(f"New tag: {new_tag}")
    if not create_and_push_tag(new_tag):
        return False

    print_success(f"Push complete. Tag: {new_tag}")
    print_info(f"Actions: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
    print_info(f"Release: https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/{new_tag}")
    return True

# ============================================================
#  MAIN
# ============================================================
def main():
    print_header("ORYEXVPN FLUTTER BUILDER + PUSHER (fully.py)")

    # 1. Generate everything
    generate_flutter_project()

    # 2. Push to GitHub (if desired)
    print_header("Push to GitHub?")
    response = input("Do you want to commit and force-push to GitHub now? (y/N): ").strip().lower()
    if response in ('y', 'yes'):
        if push_to_github():
            print_success("All done! Project is live on GitHub.")
        else:
            print_error("Push failed. Please check your network and git remote.")
            sys.exit(1)
    else:
        print_info("Skipped push. You can run 'python pusher.py' later.")
        print_info("Project files are ready in:", PROJECT_ROOT)

if __name__ == "__main__":
    main()