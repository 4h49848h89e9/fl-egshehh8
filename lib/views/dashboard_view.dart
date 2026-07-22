
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
