
import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  final int selectedIndex;
  final ValueChanged<int> onItemSelected;

  const Sidebar({
    super.key,
    required this.selectedIndex,
    required this.onItemSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 80,
      color: const Color(0xFF0A0A0A),
      child: Column(
        children: [
          const SizedBox(height: 28),
          Image.asset('assets/images/logo.png', width: 40, height: 40),
          const Spacer(),
          _buildNavItem(Icons.dashboard, 0, 'Dashboard'),
          _buildNavItem(Icons.settings, 1, 'Settings'),
          _buildNavItem(Icons.terminal, 2, 'Logs'),
          _buildNavItem(Icons.code, 3, 'Config'),
          _buildNavItem(Icons.health_and_safety, 4, 'Diagnostics'),
          const Spacer(),
          IconButton(
            icon: const Icon(Icons.send, color: Colors.grey),
            onPressed: () {},
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildNavItem(IconData icon, int index, String tooltip) {
    final isSelected = selectedIndex == index;
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 6),
      decoration: BoxDecoration(
        color: isSelected ? const Color(0xFF1E2A3A) : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
      ),
      child: IconButton(
        icon: Icon(icon, color: isSelected ? Colors.blue : Colors.grey[600]),
        onPressed: () => onItemSelected(index),
        tooltip: tooltip,
      ),
    );
  }
}
