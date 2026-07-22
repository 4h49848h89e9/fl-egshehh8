
import 'package:flutter/material.dart';

class ConnectionButton extends StatelessWidget {
  final bool isConnected;
  final bool isConnecting;
  final VoidCallback onPressed;

  const ConnectionButton({
    super.key,
    required this.isConnected,
    required this.isConnecting,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: isConnecting ? null : onPressed,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        width: 170,
        height: 170,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: isConnected ? Colors.blue : (isConnecting ? Colors.grey[800] : Colors.grey[900]),
          boxShadow: isConnected
              ? [BoxShadow(color: Colors.blue.withOpacity(0.5), blurRadius: 20, spreadRadius: 5)]
              : [],
        ),
        child: Icon(
          isConnected ? Icons.shield : (isConnecting ? Icons.wifi : Icons.power_settings_new),
          size: 76,
          color: Colors.white,
        ),
      ),
    );
  }
}
