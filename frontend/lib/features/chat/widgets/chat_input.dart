import 'package:flutter/material.dart';

class ChatInput extends StatelessWidget {

  final TextEditingController controller;
  final VoidCallback onSend;

  const ChatInput({
    super.key,
    required this.controller,
    required this.onSend,
  });

  @override
  Widget build(BuildContext context) {

    return Row(
      children: [

        Expanded(
          child: TextField(
            controller: controller,
            decoration: InputDecoration(
              hintText: "Ketik perintah untuk ZAI...",
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(15),
              ),
            ),
          ),
        ),

        const SizedBox(width:10),

        ElevatedButton(
          onPressed: onSend,
          child: const Text("KIRIM"),
        )

      ],
    );
  }
}