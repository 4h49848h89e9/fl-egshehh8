
import 'package:flutter/material.dart';
import 'package:simpleflutter/views/home_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OryvexVPN',
      theme: ThemeData.dark().copyWith(
        primaryColor: Colors.blue,
        colorScheme: const ColorScheme.dark(primary: Colors.blue),
        scaffoldBackgroundColor: const Color(0xFF0A0A0A),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0D0D0D),
          elevation: 0,
        ),
      ),
      home: const HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}
