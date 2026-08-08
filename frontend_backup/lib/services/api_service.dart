import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';

  // ============================================================
  // SEND CHAT
  // ============================================================

  static Future<String> sendMessage(String message) async {
    final response = await http
        .post(
          Uri.parse('$baseUrl/chat'),
          headers: {
            'Content-Type': 'application/json',
          },
          body: jsonEncode({
            'message': message,
          }),
        )
        .timeout(
          const Duration(seconds: 300),
        );

    if (response.statusCode != 200) {
      throw Exception(
        'Server error: ${response.statusCode}\n${response.body}',
      );
    }

    final data = jsonDecode(response.body);

    final reply = data['reply'];

    if (reply == null) {
      throw Exception('ZAI tidak memberikan jawaban.');
    }

    return reply.toString();
  }

  // ============================================================
  // GET CHAT HISTORY
  // ============================================================

  static Future<List<Map<String, dynamic>>> getHistory() async {
    final response = await http
        .get(
          Uri.parse('$baseUrl/history?limit=50'),
        )
        .timeout(
          const Duration(seconds: 30),
        );

    if (response.statusCode != 200) {
      throw Exception(
        'Gagal mengambil history: ${response.statusCode}',
      );
    }

    final data = jsonDecode(response.body);

    final messages = data['messages'];

    if (messages is! List) {
      return [];
    }

    return messages
        .whereType<Map>()
        .map(
          (item) => Map<String, dynamic>.from(item),
        )
        .toList();
  }

  // ============================================================
  // GET MEMORY
  // ============================================================

  static Future<Map<String, dynamic>> getMemory() async {
    final response = await http
        .get(
          Uri.parse('$baseUrl/memory'),
        )
        .timeout(
          const Duration(seconds: 30),
        );

    if (response.statusCode != 200) {
      throw Exception(
        'Gagal mengambil memory.',
      );
    }

    final data = jsonDecode(response.body);

    return Map<String, dynamic>.from(data);
  }

  // ============================================================
  // DELETE MEMORY
  // ============================================================

  static Future<void> clearMemory() async {
    final response = await http
        .delete(
          Uri.parse('$baseUrl/memory'),
        )
        .timeout(
          const Duration(seconds: 30),
        );

    if (response.statusCode != 200) {
      throw Exception(
        'Gagal menghapus memory.',
      );
    }
  }

  // ============================================================
  // DELETE HISTORY
  // ============================================================

  static Future<void> clearHistory() async {
    final response = await http
        .delete(
          Uri.parse('$baseUrl/history'),
        )
        .timeout(
          const Duration(seconds: 30),
        );

    if (response.statusCode != 200) {
      throw Exception(
        'Gagal menghapus history.',
      );
    }
  }
}