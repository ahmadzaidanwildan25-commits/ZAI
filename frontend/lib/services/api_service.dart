import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {

  static const url = "http://127.0.0.1:8000/chat";

  Future<String> send(String message) async {

    final response = await http.post(
      Uri.parse(url),
      headers: {
        "Content-Type":"application/json"
      },
      body: jsonEncode({
        "message":message
      }),
    );

    final json = jsonDecode(response.body);

    return json["reply"];

  }
}