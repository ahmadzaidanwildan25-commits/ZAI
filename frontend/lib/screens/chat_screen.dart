import 'package:flutter/material.dart';

import '../models/chat_message.dart';
import '../services/api_service.dart';
import '../widgets/chat_bubble.dart';
import '../widgets/message_input.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {

  final controller = TextEditingController();

  final api = ApiService();

  final List<ChatMessage> messages = [

    ChatMessage(
      text: "Halo 👋 Saya ZAI. Ada yang bisa saya bantu?",
      isUser: false,
    )

  ];

  Future send() async {

    if(controller.text.isEmpty) return;

    final text = controller.text;

    setState(() {

      messages.add(
        ChatMessage(
          text: text,
          isUser: true,
        ),
      );

    });

    controller.clear();

    final reply = await api.send(text);

    setState(() {

      messages.add(
        ChatMessage(
          text: reply,
          isUser: false,
        ),
      );

    });

  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      backgroundColor: const Color(0xff131B33),

      appBar: AppBar(
        backgroundColor: const Color(0xff101417),
        title: const Text(
          "✨ ZAI AI",
          style: TextStyle(color: Colors.white),
        ),
      ),

      body: Column(

        children: [

          Expanded(

            child: ListView.builder(

              itemCount: messages.length,

              itemBuilder: (context,index){

                return ChatBubble(
                  message: messages[index],
                );

              },

            ),

          ),

          MessageInput(
            controller: controller,
            onSend: send,
          ),

        ],

      ),

    );

  }
}