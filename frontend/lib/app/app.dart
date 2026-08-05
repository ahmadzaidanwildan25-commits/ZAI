import 'package:flutter/material.dart';
import 'theme.dart';
import '../features/chat/screens/chat_screen.dart';

class ZAIApp extends StatelessWidget {
  const ZAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "ZAI",
      debugShowCheckedModeBanner: false,
      theme: zaiTheme,
      home: const ChatScreen(),
    );
  }
}