import 'package:flutter/material.dart';
import '../models/chat_message.dart';

class ChatBubble extends StatelessWidget {
  final ChatMessage message;

  const ChatBubble({
    Key? key,
    required this.message,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment:
          message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: const BoxConstraints(maxWidth: 500),
        decoration: BoxDecoration(
          color: message.isUser
              ? const Color(0xFF14B8D4)
              : const Color(0xFF2B3352),
          borderRadius: BorderRadius.circular(18),
        ),
        child: Text(
          message.text,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 17,
          ),
        ),
      ),
    );
  }
}