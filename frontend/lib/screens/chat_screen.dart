import 'package:flutter/material.dart';

import '../services/api_service.dart';

class ChatMessage {
  final String text;
  final bool isUser;

  ChatMessage({
    required this.text,
    required this.isUser,
  });
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({
    super.key,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  // ============================================================
  // CONTROLLERS
  // ============================================================

  final TextEditingController _controller =
      TextEditingController();

  final ScrollController _scrollController =
      ScrollController();

  // ============================================================
  // CHAT DATA
  // ============================================================

  final List<ChatMessage> _messages = [];

  bool _isLoading = false;

  // ============================================================
  // INIT
  // ============================================================

  @override
  void initState() {
    super.initState();

    // Sengaja TIDAK memanggil _loadHistory().
    //
    // Tujuannya:
    // Saat ZAI pertama dibuka, layar langsung bersih
    // dan menampilkan welcome screen.
  }

  // ============================================================
  // SEND MESSAGE
  // ============================================================

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();

    // Jangan kirim pesan kosong
    // dan jangan kirim ketika ZAI masih memproses.
    if (text.isEmpty || _isLoading) {
      return;
    }

    // Bersihkan input.
    _controller.clear();

    // Tampilkan pesan user.
    setState(() {
      _messages.add(
        ChatMessage(
          text: text,
          isUser: true,
        ),
      );

      _isLoading = true;
    });

    _scrollToBottom();

    try {
      // Kirim pesan ke backend / AI.
      final reply = await ApiService.sendMessage(text);

      if (!mounted) return;

      // Tampilkan jawaban ZAI.
      setState(() {
        _messages.add(
          ChatMessage(
            text: reply,
            isUser: false,
          ),
        );

        _isLoading = false;
      });

      _scrollToBottom();
    } catch (error) {
      if (!mounted) return;

      // Tampilkan error sebagai pesan ZAI.
      setState(() {
        _messages.add(
          ChatMessage(
            text:
                'Maaf, ZAI mengalami masalah.\n\n$error',
            isUser: false,
          ),
        );

        _isLoading = false;
      });

      _scrollToBottom();
    }
  }

  // ============================================================
  // SCROLL
  // ============================================================

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback(
      (_) {
        if (!_scrollController.hasClients) {
          return;
        }

        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(
            milliseconds: 300,
          ),
          curve: Curves.easeOut,
        );
      },
    );
  }

  // ============================================================
  // MESSAGE BUBBLE
  // ============================================================

  Widget _messageBubble(
    ChatMessage message,
  ) {
    return Align(
      alignment: message.isUser
          ? Alignment.centerRight
          : Alignment.centerLeft,
      child: Container(
        constraints: const BoxConstraints(
          maxWidth: 700,
        ),
        margin: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 6,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 18,
          vertical: 13,
        ),
        decoration: BoxDecoration(
          color: message.isUser
              ? const Color(0xFF2563EB)
              : const Color(0xFF1E293B),
          borderRadius: BorderRadius.circular(18),
          border: Border.all(
            color: Colors.white.withValues(
              alpha: 0.08,
            ),
          ),
        ),
        child: SelectableText(
          message.text,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 15,
            height: 1.5,
          ),
        ),
      ),
    );
  }

  // ============================================================
  // LOADING BUBBLE
  // ============================================================

  Widget _loadingBubble() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 6,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 18,
          vertical: 13,
        ),
        decoration: BoxDecoration(
          color: const Color(0xFF1E293B),
          borderRadius: BorderRadius.circular(18),
        ),
        child: const Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              width: 16,
              height: 16,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: Colors.white70,
              ),
            ),
            SizedBox(width: 12),
            Text(
              'ZAI sedang berpikir...',
              style: TextStyle(
                color: Colors.white70,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ============================================================
  // BUILD
  // ============================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF020617),

      // ========================================================
      // APP BAR
      // ========================================================

      appBar: AppBar(
        backgroundColor: const Color(0xFF020617),
        elevation: 0,
        centerTitle: false,

        title: const Row(
          children: [
            CircleAvatar(
              radius: 18,
              backgroundColor: Color(0xFF2563EB),
              child: Icon(
                Icons.smart_toy,
                color: Colors.white,
                size: 21,
              ),
            ),

            SizedBox(width: 12),

            Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,
              children: [
                Text(
                  'ZAI',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                Text(
                  'ONLINE • QWEN3:8B',
                  style: TextStyle(
                    color: Colors.greenAccent,
                    fontSize: 10,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),

      // ========================================================
      // BODY
      // ========================================================

      body: Column(
        children: [
          // ====================================================
          // CHAT AREA
          // ====================================================

          Expanded(
            child: _messages.isEmpty
                ? _welcomeScreen()
                : ListView.builder(
                    controller: _scrollController,

                    padding:
                        const EdgeInsets.only(
                      top: 20,
                      bottom: 20,
                    ),

                    itemCount:
                        _messages.length +
                            (_isLoading ? 1 : 0),

                    itemBuilder:
                        (context, index) {
                      // Loading bubble
                      if (
                        _isLoading &&
                        index ==
                            _messages.length
                      ) {
                        return _loadingBubble();
                      }

                      // Chat bubble
                      return _messageBubble(
                        _messages[index],
                      );
                    },
                  ),
          ),

          // ====================================================
          // INPUT AREA
          // ====================================================

          SafeArea(
            child: Container(
              padding:
                  const EdgeInsets.fromLTRB(
                12,
                8,
                12,
                12,
              ),

              decoration:
                  BoxDecoration(
                color: const Color(0xFF0F172A),

                border: Border(
                  top: BorderSide(
                    color:
                        Colors.white.withValues(
                      alpha: 0.06,
                    ),
                  ),
                ),
              ),

              child: Row(
                crossAxisAlignment:
                    CrossAxisAlignment.end,

                children: [
                  // ==================================================
                  // TEXT INPUT
                  // ==================================================

                  Expanded(
                    child: TextField(
                      controller: _controller,

                      minLines: 1,
                      maxLines: 5,

                      style:
                          const TextStyle(
                        color: Colors.white,
                      ),

                      textInputAction:
                          TextInputAction.newline,

                      decoration:
                          InputDecoration(
                        hintText:
                            'Ketik pesan untuk ZAI...',

                        hintStyle:
                            const TextStyle(
                          color: Colors.white38,
                        ),

                        filled: true,

                        fillColor:
                            const Color(
                          0xFF1E293B,
                        ),

                        border:
                            OutlineInputBorder(
                          borderRadius:
                              BorderRadius.circular(
                            20,
                          ),

                          borderSide:
                              BorderSide.none,
                        ),

                        contentPadding:
                            const EdgeInsets
                                .symmetric(
                          horizontal: 18,
                          vertical: 13,
                        ),
                      ),

                      onSubmitted: (_) {
                        _sendMessage();
                      },
                    ),
                  ),

                  const SizedBox(width: 8),

                  // ==================================================
                  // SEND BUTTON
                  // ==================================================

                  GestureDetector(
                    onTap: _isLoading
                        ? null
                        : _sendMessage,

                    child: Container(
                      width: 50,
                      height: 50,

                      decoration:
                          BoxDecoration(
                        color: _isLoading
                            ? Colors.grey
                            : const Color(
                                0xFF2563EB,
                              ),

                        shape:
                            BoxShape.circle,
                      ),

                      child:
                          const Icon(
                        Icons.arrow_upward,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ============================================================
  // WELCOME SCREEN
  // ============================================================

  Widget _welcomeScreen() {
    return Center(
      child: SingleChildScrollView(
        padding:
            const EdgeInsets.all(30),

        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,

          children: [
            // ==================================================
            // ZAI ICON
            // ==================================================

            Container(
              width: 90,
              height: 90,

              decoration:
                  BoxDecoration(
                shape:
                    BoxShape.circle,

                color:
                    const Color(
                  0xFF2563EB,
                ).withValues(
                  alpha: 0.15,
                ),

                border:
                    Border.all(
                  color:
                      const Color(
                    0xFF2563EB,
                  ),
                  width: 2,
                ),
              ),

              child:
                  const Icon(
                Icons.smart_toy,
                size: 48,
                color:
                    Color(
                  0xFF60A5FA,
                ),
              ),
            ),

            const SizedBox(
              height: 25,
            ),

            // ==================================================
            // ZAI TITLE
            // ==================================================

            const Text(
              'ZAI',

              style:
                  TextStyle(
                color:
                    Colors.white,

                fontSize:
                    34,

                fontWeight:
                    FontWeight.bold,

                letterSpacing:
                    4,
              ),
            ),

            const SizedBox(
              height: 8,
            ),

            // ==================================================
            // SUBTITLE
            // ==================================================

            const Text(
              'Personal AI Assistant',

              style:
                  TextStyle(
                color:
                    Colors.white54,

                fontSize:
                    15,
              ),
            ),

            const SizedBox(
              height: 30,
            ),

            // ==================================================
            // GREETING
            // ==================================================

            const Text(
              'Halo, Zaidan 👋',

              style:
                  TextStyle(
                color:
                    Colors.white,

                fontSize:
                    21,

                fontWeight:
                    FontWeight.w600,
              ),
            ),

            const SizedBox(
              height: 8,
            ),

            // ==================================================
            // WELCOME TEXT
            // ==================================================

            const Text(
              'Ada yang bisa ZAI bantu hari ini?',

              textAlign:
                  TextAlign.center,

              style:
                  TextStyle(
                color:
                    Colors.white54,

                fontSize:
                    14,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ============================================================
  // DISPOSE
  // ============================================================

  @override
  void dispose() {
    _controller.dispose();

    _scrollController.dispose();

    super.dispose();
  }
}