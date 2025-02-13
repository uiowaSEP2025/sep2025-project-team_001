import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTextStyles {
  static TextStyle bigBoldLetters(double screenHeight, Color color) {
    return GoogleFonts.roboto(
        fontWeight: FontWeight.bold, fontSize: screenHeight * 0.05, color: color);
  }

  static TextStyle subtitleParagraph(double screenHeight, Color color) {
    return GoogleFonts.roboto(
        fontWeight: FontWeight.w400, fontSize: screenHeight * 0.025, color: color);
  }

  static TextStyle textFieldLabel(double screenHeight, Color color) {
    return GoogleFonts.roboto(
        fontWeight: FontWeight.bold, fontSize: screenHeight * 0.02, color: color);
  }

  static TextStyle buttonText(double screenHeight, Color color) {
    return GoogleFonts.roboto(
        fontWeight: FontWeight.bold, fontSize: screenHeight * 0.022, color: color);
  }
}
