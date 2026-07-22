
import 'dart:async';
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
  late Timer _timer;
  TrafficStats _stats = TrafficStats.zero();

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) async {
      final stats = await _vpnService.getTrafficStats();
      setState(() {
        _stats = stats;
      });
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

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
            children: [
              Expanded(child: StatsCard(icon: Icons.speed, label: 'LATENCY', value: _stats.ping)),
              Expanded(child: StatsCard(icon: Icons.arrow_downward, label: 'DOWNLOAD', value: _stats.downloadSpeed)),
              Expanded(child: StatsCard(icon: Icons.arrow_upward, label: 'UPLOAD', value: _stats.uploadSpeed)),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(child: StatsCard(icon: Icons.cloud_download, label: 'TOTAL DOWN', value: _stats.downloadTotal)),
              Expanded(child: StatsCard(icon: Icons.cloud_upload, label: 'TOTAL UP', value: _stats.uploadTotal)),
              Expanded(child: const StatsCard(icon: Icons.timer, label: 'UPTIME', value: '00:00:00')),
            ],
          ),
        ],
      ),
    );
  }
}
