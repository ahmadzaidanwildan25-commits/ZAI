import 'package:flutter/material.dart';
import 'screens/chat_screen.dart';

void main() {
  runApp(const ZAIApp());
}

class ZAIApp extends StatelessWidget {
  const ZAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "ZAI",
      theme: ThemeData.dark(),
      home: const ChatScreen(),
    );
  }
}