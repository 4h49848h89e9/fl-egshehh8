
import 'package:flutter/material.dart';
import 'package:simpleflutter/services/vpn_service.dart';

class LogsView extends StatefulWidget {
  const LogsView({super.key});

  @override
  State<LogsView> createState() => _LogsViewState();
}

class _LogsViewState extends State<LogsView> {
  final VpnService _vpn = VpnService();
  String _logs = '--- ORYEXVPN SYSTEM LOGS STACK ---';

  @override
  void initState() {
    super.initState();
    _vpn.getLogs().listen((log) {
      setState(() {
        _logs = log;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          Row(
            children: [
              const Icon(Icons.terminal, color: Colors.blue),
              const SizedBox(width: 8),
              const Text('System Console', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () async {
                  await _vpn.clearLogs();
                },
              ),
            ],
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.black26,
                borderRadius: BorderRadius.circular(12),
              ),
              child: SingleChildScrollView(
                child: Text(
                  _logs,
                  style: const TextStyle(fontFamily: 'monospace', fontSize: 13, color: Colors.greenAccent),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
