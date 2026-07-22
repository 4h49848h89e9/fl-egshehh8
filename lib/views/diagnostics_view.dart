
import 'package:flutter/material.dart';
import 'package:simpleflutter/services/vpn_service.dart';

class DiagnosticsView extends StatefulWidget {
  const DiagnosticsView({super.key});

  @override
  State<DiagnosticsView> createState() => _DiagnosticsViewState();
}

class _DiagnosticsViewState extends State<DiagnosticsView> {
  final VpnService _vpn = VpnService();
  String _output = 'Press DIAGNOSE to begin scan.';
  bool _running = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 3,
            child: Column(
              children: [
                const Text('DIAGNOSTICS CHECKLIST', style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                _buildCheckItem('Xray Core Binary', 'xray.exe exists'),
                _buildCheckItem('Proxy Inbound Port', 'Port 10808 free'),
                _buildCheckItem('SSL Root CA Trust', 'Certificate installed'),
                _buildCheckItem('Registry Proxy Config', 'System proxy aligned'),
                _buildCheckItem('Internet Connection', 'Outbound connectivity'),
              ],
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            flex: 2,
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black26,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  const Text('DIAGNOSTICS OUTPUT', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Expanded(
                    child: SingleChildScrollView(
                      child: Text(_output, style: const TextStyle(fontSize: 12, fontFamily: 'monospace')),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: _running ? null : () async {
                      setState(() => _running = true);
                      final result = await _vpn.runDiagnostics();
                      setState(() {
                        _output = result;
                        _running = false;
                      });
                    },
                    child: _running ? const CircularProgressIndicator() : const Text('DIAGNOSE'),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCheckItem(String title, String desc) {
    return ListTile(
      leading: const Icon(Icons.check_circle_outline, color: Colors.blue),
      title: Text(title),
      subtitle: Text(desc, style: const TextStyle(fontSize: 12)),
    );
  }
}
