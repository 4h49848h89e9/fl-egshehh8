
import 'dart:async';
import 'dart:convert';
import 'package:flutter/services.dart';

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

  Future<Map<String, String>> getTrafficStats() async {
    final stats = await _channel.invokeMethod('getTrafficStats');
    return Map<String, String>.from(stats);
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
