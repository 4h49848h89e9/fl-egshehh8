import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Simple Flutter App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  void _launchURL(String url) async {
    final Uri uri = Uri.parse(url);
    try {
      if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
        throw Exception('Could not launch $url');
      }
    } catch (e) {
      print('Error launching URL: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Simple Flutter App'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const SizedBox(height: 20),
                
                // Logo
                Container(
                  width: 120,
                  height: 120,
                  decoration: BoxDecoration(
                    color: Colors.blue.shade50,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.flutter_dash,
                    size: 80,
                    color: Colors.blue,
                  ),
                ),
                const SizedBox(height: 24),
                
                // Title
                const Text(
                  'Simpleflutter',
                  style: TextStyle(
                    fontSize: 36,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF1a1a2e),
                  ),
                ),
                const SizedBox(height: 8),
                const Text(
                  'A modern Flutter Windows application',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey,
                  ),
                ),
                const SizedBox(height: 30),
                
                // Badges
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  alignment: WrapAlignment.center,
                  children: const [
                    _Badge(text: 'Flutter', color: Colors.green),
                    _Badge(text: 'Windows 10/11', color: Colors.blue),
                    _Badge(text: 'v1.0.0', color: Colors.orange),
                    _Badge(text: '⚡ GitHub Actions', color: null),
                  ],
                ),
                const SizedBox(height: 35),
                
                // Feature Grid
                GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    childAspectRatio: 2.5,
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                  ),
                  itemCount: _features.length,
                  itemBuilder: (context, index) {
                    return _FeatureCard(feature: _features[index]);
                  },
                ),
                const SizedBox(height: 35),
                
                // Buttons
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Expanded(
                      child: _ActionButton(
                        text: '⬇️ Download Latest',
                        color: Colors.blue,
                        onPressed: () => _launchURL(
                          'https://github.com/4h49848h89e9/fl-egshehh8/releases'
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: _ActionButton(
                        text: 'View on GitHub',
                        color: const Color(0xFF24292e),
                        onPressed: () => _launchURL(
                          'https://github.com/4h49848h89e9/fl-egshehh8'
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 30),
                
                // Version info
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.grey.shade300),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.info_outline, size: 16, color: Colors.grey),
                      SizedBox(width: 8),
                      Text(
                        'simpleflutter • Built with ❤️ using Flutter • 2026',
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// Badge Widget
class _Badge extends StatelessWidget {
  final String text;
  final Color? color;

  const _Badge({required this.text, this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (color != null) ...[
            Container(
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: color,
              ),
            ),
            const SizedBox(width: 8),
          ],
          Text(
            text,
            style: const TextStyle(
              fontSize: 13,
              color: Color(0xFF555555),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}

// Feature Card Widget
class _FeatureCard extends StatelessWidget {
  final Feature feature;

  const _FeatureCard({required this.feature});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Row(
        children: [
          Text(feature.icon, style: const TextStyle(fontSize: 28)),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  feature.title,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF1a1a2e),
                  ),
                ),
                Text(
                  feature.subtitle,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Colors.grey,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Action Button Widget
class _ActionButton extends StatelessWidget {
  final String text;
  final Color color;
  final VoidCallback onPressed;

  const _ActionButton({
    required this.text,
    required this.color,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        elevation: 2,
      ),
      child: Text(
        text,
        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
      ),
    );
  }
}

// Feature Data Model
class Feature {
  final String icon;
  final String title;
  final String subtitle;

  const Feature({
    required this.icon,
    required this.title,
    required this.subtitle,
  });
}

// Feature Data
const List<Feature> _features = [
  Feature(
    icon: '📱',
    title: 'Flutter Framework',
    subtitle: 'Built with Flutter stable channel',
  ),
  Feature(
    icon: '🖥️',
    title: 'Windows Native',
    subtitle: 'Fully integrated Windows desktop app',
  ),
  Feature(
    icon: '🚀',
    title: 'CI/CD Ready',
    subtitle: 'Automated builds with GitHub Actions',
  ),
  Feature(
    icon: '📦',
    title: 'Easy Releases',
    subtitle: 'One-command releases with tags',
  ),
];