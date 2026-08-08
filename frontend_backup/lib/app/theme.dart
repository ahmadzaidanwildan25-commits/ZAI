import 'package:flutter/material.dart';

final ThemeData zaiTheme = ThemeData(
  brightness: Brightness.dark,
  scaffoldBackgroundColor: const Color(0xff0f172a),
  primaryColor: Colors.cyan,
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.cyan,
    brightness: Brightness.dark,
  ),
  useMaterial3: true,
);