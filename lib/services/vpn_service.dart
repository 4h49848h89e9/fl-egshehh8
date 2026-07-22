
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
