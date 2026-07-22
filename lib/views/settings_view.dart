
import 'package:flutter/material.dart';
import 'package:simpleflutter/services/vpn_service.dart';

class SettingsView extends StatefulWidget {
  const SettingsView({super.key});

  @override
  State<SettingsView> createState() => _SettingsViewState();
}

class _SettingsViewState extends State<SettingsView> {
  final VpnService _vpn = VpnService();
  bool _dnsLog = false;
  bool _accessLog = false;
  bool _googleSwitcher = false;
  bool _useHttp2 = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Settings', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 20),
          SwitchListTile(
            title: const Text('DNS Query Logging'),
            subtitle: const Text('Log resolved hosts in console'),
            value: _dnsLog,
            onChanged: (v) => setState(() => _dnsLog = v),
          ),
          SwitchListTile(
            title: const Text('Access Connection Logging'),
            subtitle: const Text('Log proxy access details'),
            value: _accessLog,
            onChanged: (v) => setState(() => _accessLog = v),
          ),
          SwitchListTile(
            title: const Text('Enable Google IP Switcher'),
            subtitle: const Text('Enables IP Switcher tab'),
            value: _googleSwitcher,
            onChanged: (v) => setState(() => _googleSwitcher = v),
          ),
          SwitchListTile(
            title: const Text('Use HTTP/2 for Special Mode'),
            subtitle: const Text('Use TCP instead of UDP/QUIC'),
            value: _useHttp2,
            onChanged: (v) => setState(() => _useHttp2 = v),
          ),
          const Spacer(),
          ElevatedButton.icon(
            onPressed: () async {
              await _vpn.uninstallCertificate();
            },
            icon: const Icon(Icons.delete_forever),
            label: const Text('UNINSTALL CERTIFICATE'),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
          ),
        ],
      ),
    );
  }
}
