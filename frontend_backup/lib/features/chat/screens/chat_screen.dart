import 'package:flutter/material.dart';

import '../models/chat_message.dart';
import '../widgets/chat_bubble.dart';
import '../widgets/chat_input.dart';
import '../services/chat_service.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController controller = TextEditingController();

  final ChatService service = ChatService();

  final List<ChatMessage> messages = [
    ChatMessage(
      text: "Halo 👋 Saya ZAI. Ada yang bisa saya bantu?",
      isUser: false,
      time: DateTime.now(),
    ),
  ];

  bool isLoading = false;

  void sendMessage() {
    final text = controller.text.trim();

    if (text.isEmpty || isLoading) {
      return;
    }

    setState(() {
      messages.add(
        ChatMessage(
          text: text,
          isUser: true,
          time: DateTime.now(),
        ),
      );

      isLoading = true;
    });

    controller.clear();

    service.sendMessage(text).then((reply) {
      if (!mounted) return;

      setState(() {
        messages.add(
          ChatMessage(
            text: reply,
            isUser: false,
            time: DateTime.now(),
          ),
        );

        isLoading = false;
      });
    }).catchError((error) {
      if (!mounted) return;

      setState(() {
        messages.add(
          ChatMessage(
            text: "Maaf, terjadi kesalahan saat menghubungkan ke server.",
            isUser: false,
            time: DateTime.now(),
          ),
        );

        isLoading = false;
      });
    });
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
            Icon(Icons.auto_awesome),
            SizedBox(width: 10),
            Text("ZAI AI"),
          ],
        ),
      ),

      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: messages.length,
                itemBuilder: (context, index) {
                  return ChatBubble(
                    message: messages[index],
                  );
                },
              ),
            ),

            if (isLoading)
              const Padding(
                padding: EdgeInsets.only(
                  left: 20,
                  right: 20,
                  bottom: 8,
                ),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                        ),
                      ),
                      SizedBox(width: 10),
                      Text("ZAI sedang berpikir..."),
                    ],
                  ),
                ),
              ),

            ChatInput(
              controller: controller,
              onSend: sendMessage,
            ),
          ],
        ),
      ),
    );
  }
}