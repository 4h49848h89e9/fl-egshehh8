
import 'dart:async';
import 'dart:convert';
import 'package:flutter/services.dart';

class TrafficStats {
  final String ping;
  final String downloadSpeed;
  final String uploadSpeed;
  final String downloadTotal;
  final String uploadTotal;

  TrafficStats({
    required this.ping,
    required this.downloadSpeed,
    required this.uploadSpeed,
    required this.downloadTotal,
    required this.uploadTotal,
  });

  factory TrafficStats.fromMap(Map<String, dynamic> map) {
    return TrafficStats(
      ping: map['ping'] ?? '-- ms',
      downloadSpeed: map['downloadSpeed'] ?? '0 B/s',
      uploadSpeed: map['uploadSpeed'] ?? '0 B/s',
      downloadTotal: map['downloadTotal'] ?? '0 B',
      uploadTotal: map['uploadTotal'] ?? '0 B',
    );
  }

  factory TrafficStats.zero() {
    return TrafficStats(
      ping: '-- ms',
      downloadSpeed: '0 B/s',
      uploadSpeed: '0 B/s',
      downloadTotal: '0 B',
      uploadTotal: '0 B',
    );
  }
}

class VpnService {
  static const MethodChannel _channel = MethodChannel('com.oryvexvpn/vpn');

  bool _isConnected = false;
  bool _isConnecting = false;

  bool get isConnected => _isConnected;
  bool get isConnecting => _isConnecting;

  final StreamController<String> _logController = StreamController<String>.broadcast();

  VpnService() {
    _channel.setMethodCallHandler(_handleMethodCall);
  }

  Future<void> _handleMethodCall(MethodCall call) async {
    if (call.method == 'onLog') {
      _logController.add(call.arguments);
    }
  }

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
      // handle
    } finally {
      _isConnecting = false;
    }
  }

  Future<TrafficStats> getTrafficStats() async {
    final map = await _channel.invokeMethod('getTrafficStats');
    return TrafficStats.fromMap(Map<String, dynamic>.from(map));
  }

  Stream<String> getLogs() => _logController.stream;

  Future<void> clearLogs() async {
    await _channel.invokeMethod('clearLogs');
  }

  Future<String> getConfig() async {
    return await _channel.invokeMethod('getConfig');
  }

  Future<void> saveConfig(String config) async {
    await _channel.invokeMethod('saveConfig', config);
  }

  Future<void> uninstallCertificate() async {
    await _channel.invokeMethod('uninstallCertificate');
  }

  Future<String> runDiagnostics() async {
    return await _channel.invokeMethod('runDiagnostics');
  }
}
