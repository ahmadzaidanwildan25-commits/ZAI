import 'package:flutter/material.dart';

class MessageInput extends StatelessWidget {
  final TextEditingController controller;
  final VoidCallback onSend;

  const MessageInput({
    super.key,
    required this.controller,
    required this.onSend,
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Row(
          children: [

            Expanded(
              child: TextField(
                controller: controller,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  hintText: "Ketik pesan...",
                  hintStyle:
                      const TextStyle(color: Colors.white54),
                  filled: true,
                  fillColor: const Color(0xff1A2038),
                  border: OutlineInputBorder(
                    borderRadius:
                        BorderRadius.circular(20),
                  ),
                ),
              ),
            ),

            const SizedBox(width: 10),

            ElevatedButton(
              onPressed: onSend,
              child: const Text("KIRIM"),
            )

          ],
        ),
      ),
    );
  }
}