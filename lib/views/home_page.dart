
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
