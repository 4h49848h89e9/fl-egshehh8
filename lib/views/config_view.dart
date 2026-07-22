
import 'package:flutter/material.dart';
import 'package:simpleflutter/services/vpn_service.dart';

class ConfigView extends StatefulWidget {
  const ConfigView({super.key});

  @override
  State<ConfigView> createState() => _ConfigViewState();
}

class _ConfigViewState extends State<ConfigView> {
  final VpnService _vpn = VpnService();
  String _config = 'Loading...';

  @override
  void initState() {
    super.initState();
    _loadConfig();
  }

  Future<void> _loadConfig() async {
    final cfg = await _vpn.getConfig();
    setState(() {
      _config = cfg;
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
              const Icon(Icons.code, color: Colors.blue),
              const SizedBox(width: 8),
              const Text('Advanced Configuration', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const Spacer(),
              IconButton(
                icon: const Icon(Icons.refresh),
                onPressed: _loadConfig,
              ),
              IconButton(
                icon: const Icon(Icons.save),
                onPressed: () async {
                  await _vpn.saveConfig(_config);
                },
              ),
            ],
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black26,
                borderRadius: BorderRadius.circular(12),
              ),
              child: TextField(
                controller: TextEditingController(text: _config),
                onChanged: (value) => _config = value,
                maxLines: null,
                expands: true,
                style: const TextStyle(fontFamily: 'monospace', fontSize: 13, color: Colors.white),
                decoration: const InputDecoration(border: InputBorder.none),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
