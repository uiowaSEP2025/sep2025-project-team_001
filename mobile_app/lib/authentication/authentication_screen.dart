import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/design/app_colors.dart';
import 'package:mobile_app/design/app_text_styles.dart';

class AuthenticationPage extends StatefulWidget {
  const AuthenticationPage({super.key});

  @override
  State<AuthenticationPage> createState() => _AuthenticationPageState();
}

class _AuthenticationPageState extends State<AuthenticationPage> {
  late TextEditingController _emailController;
  late TextEditingController _passwordController;
  String email = "";
  String password = "";
  bool isLoading = false;

  final Dio _dio = Dio();
  final String apiUrl = "http://localhost:8000/auth/login/";

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Scaffold(
        body: GestureDetector(
      onTap: () {
        FocusManager.instance.primaryFocus
            ?.unfocus(); //unfocus to close keyboard
      },
      child: Container(
        width: screenWidth,
        height: screenHeight,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xff1A1D1A), Color(0xff313538)], // Gradient colors
            begin: Alignment.topLeft, // Gradient start position
            end: Alignment.bottomRight, // Gradient end position
          ),
        ),
        child: SingleChildScrollView(
          physics: AlwaysScrollableScrollPhysics(),
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
            SizedBox(
              height: screenHeight * 0.1,
            ),
            Container(
              width: screenWidth * 0.6,
              child: Image.asset("assets/images/StreamlineLogo.png"),
            ),
            SizedBox(
              height: verticalSpacing / 2,
            ),
            Container(
              width: screenWidth * 0.75,
              child: Text(
                "Please sign in to start enjoying special treatment from your favorite restaurant",
                textAlign: TextAlign.center,
                style: AppTextStyles.subtitleParagraph(
                    screenHeight, AppColors.whiteText),
              ),
            ),
            SizedBox(
              height: verticalSpacing,
            ),
            Padding(
              padding: EdgeInsets.only(
                  left: horizontalSpacing, right: horizontalSpacing),
              child: InputTextBox(
                label: "Email",
                hintText: "johndoe@gmail.com",
                screenWidth: screenWidth,
                screenHeight: screenHeight,
                controller: _emailController,
                onSubmitted: authenticate,
              ),
            ),
            SizedBox(
              height: verticalSpacing,
            ),
            Padding(
              padding: EdgeInsets.only(
                  left: horizontalSpacing, right: horizontalSpacing),
              child: InputTextBox(
                label: "Password",
                hintText: "********",
                screenWidth: screenWidth,
                screenHeight: screenHeight,
                controller: _passwordController,
                onSubmitted: authenticate,
              ),
            ),
            SizedBox(
              height: verticalSpacing * 2,
            ),
            Container(
              height: screenWidth * 0.12,
              width: screenWidth - horizontalSpacing * 2,
              child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryColor),
                  onPressed: isLoading ? null : authenticate,
                  child: isLoading
                      ? CircularProgressIndicator(color: Colors.white)
                      : Center(
                          child: Text(
                            "SIGN UP/LOGIN",
                            style: AppTextStyles.buttonText(
                                screenHeight, AppColors.whiteText),
                          ),
                        )),
            ),
            SizedBox(
              height: verticalSpacing * 2,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  height: 1,
                  width: screenWidth * 0.3,
                  decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        AppColors.backgroundColor,
                        Color(0xffD9D9D9)
                      ], // Gradient colors
                      begin: Alignment.topLeft, // Gradient start position
                      end: Alignment.bottomRight, // Gradient end position
                    ),
                  ),
                ),
                SizedBox(
                  width: horizontalSpacing / 2,
                ),
                Text(
                  "Or continue with",
                  style: AppTextStyles.subtitleParagraph(
                      screenHeight, AppColors.whiteText),
                ),
                SizedBox(
                  width: horizontalSpacing / 2,
                ),
                Container(
                  height: 1,
                  width: screenWidth * 0.3,
                  decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        AppColors.backgroundColor,
                        Color(0xffD9D9D9)
                      ], // Gradient colors
                      begin: Alignment.bottomRight, // Gradient start position
                      end: Alignment.bottomLeft, // Gradient end position
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(
              height: verticalSpacing,
            ),
            (Platform.isIOS)
                ? Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                          height: screenWidth * 0.15,
                          width: screenWidth * 0.15,
                          decoration: BoxDecoration(
                              border: Border.all(
                                color: AppColors.whiteText, // Border color
                                width: 2, // Border width
                              ),
                              borderRadius: BorderRadius.circular(10)),
                          child: Image.asset("assets/logos/GoogleLogo.png")),
                      SizedBox(
                        width: horizontalSpacing * 2,
                      ),
                      Container(
                        height: screenWidth * 0.15,
                        width: screenWidth * 0.15,
                        decoration: BoxDecoration(
                            border: Border.all(
                              color: AppColors.whiteText, // Border color
                              width: 2, // Border width
                            ),
                            borderRadius: BorderRadius.circular(10)),
                        child: Icon(
                          Icons.apple,
                          size: screenWidth * 0.11,
                          color: AppColors.whiteText,
                        ),
                      ),
                    ],
                  )
                : Container(
                    height: screenWidth * 0.15,
                    width: screenWidth * 0.15,
                    decoration: BoxDecoration(
                        border: Border.all(
                          color: AppColors.whiteText,
                          width: 2, 
                        ),
                        borderRadius: BorderRadius.circular(10)),
                    child: Image.asset("assets/logos/GoogleLogo.png")),
          ]),
        ),
      ),
    ));
  }

  void authenticate() async {
    String email = _emailController.text.trim();
    String password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Please enter email and password")),
      );
      return;
    }

    setState(() => isLoading = true);

    try {
      Response response = await _dio.post(
        apiUrl,
        data: {"username": email, "password": password},
        options: Options(headers: {"Content-Type": "application/json"}),
      );

      print("Login successful: ${response.data}"); //

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Login Successful!")),
      );

      Navigator.pushReplacementNamed(context, "/home");
    } catch (error) {
      print("Login error: $error");

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Invalid email or password")),
      );
    }

    setState(() => isLoading = false);
  }
}

class InputTextBox extends StatelessWidget {
  const InputTextBox(
      {super.key,
      required this.screenWidth,
      required this.screenHeight,
      required this.label,
      required this.hintText,
      required this.controller,
      required this.onSubmitted});

  final double screenWidth;
  final double screenHeight;
  final String label;
  final String hintText;
  final TextEditingController controller;
  final VoidCallback onSubmitted;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Text(
              label,
              style: AppTextStyles.textFieldLabel(
                  screenHeight, AppColors.whiteText),
            ),
          ],
        ),
        Container(
          height: screenWidth * 0.12,
          child: TextField(
            onSubmitted: (value) {
              onSubmitted();
            },
            controller: controller,
            cursorColor: AppColors.primaryColor,
            decoration: InputDecoration(
                filled: true,
                fillColor: AppColors.whiteText,
                border: OutlineInputBorder(),
                hintText: hintText),
          ),
        ),
      ],
    );
  }
}
