import 'dart:convert';

import 'package:http/http.dart' as http;

import '../../../core/api.dart';

class ChatService {

  Future<String> sendMessage(String message) async {

    final response = await http.post(

      Uri.parse("$apiUrl/chat"),

      headers: {

        "Content-Type":"application/json",

      },

      body: jsonEncode({

        "message":message

      }),

    );

    if(response.statusCode==200){

      final data=jsonDecode(response.body);

      return data["reply"];

    }

    return "Server Error";

  }

}