import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';
import 'dart:ui';

import 'package:mobile_app/design/widgets/user_input/password_text_box.dart';

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

    return AnnotatedRegion<SystemUiOverlayStyle>(
      value: SystemUiOverlayStyle(
          statusBarColor: Colors.white, statusBarBrightness: Brightness.dark),
      child: Scaffold(
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          title: StreamlineLogo(
            screenHeight: screenHeight,
            color: Colors.white,
          ),
          backgroundColor: Colors.transparent,
          scrolledUnderElevation: 0,
        ),
        backgroundColor: Colors.white,
        body: GestureDetector(
          onTap: () {
            FocusManager.instance.primaryFocus?.unfocus();
          },
          child: Stack(children: [
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              child: ImageFiltered(
                imageFilter: ImageFilter.blur(sigmaX: 2, sigmaY: 2),
                child: Container(
                  height: screenHeight * 0.25,
                  clipBehavior: Clip.hardEdge,
                  decoration: const BoxDecoration(
                    borderRadius:
                        BorderRadius.vertical(bottom: Radius.circular(0)),
                  ),
                  child: Image.asset(
                    "assets/images/partyDancingPicture.jpg",
                    fit: BoxFit.cover,
                    width: double.infinity,
                  ),
                ),
              ),
            ),
            Positioned.fill(
              child: SingleChildScrollView(
                physics: AlwaysScrollableScrollPhysics(),
                child: Column(
                  children: [
                    SizedBox(
                      height: screenHeight * 0.25,
                    ),
                    Container(
                      color: Colors.white,
                      child: Column(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            SizedBox(
                              height: verticalSpacing / 2,
                            ),
                            Container(
                              width: screenWidth * 0.75,
                              child: Text(
                                "Sign in",
                                textAlign: TextAlign.center,
                                style: AppTextStyles.bigBoldLetters(
                                    screenHeight * 0.7, Colors.black),
                              ),
                            ),
                            SizedBox(
                              height: verticalSpacing / 2,
                            ),
                            Padding(
                              padding: EdgeInsets.only(
                                  left: horizontalSpacing,
                                  right: horizontalSpacing),
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
                                  left: horizontalSpacing,
                                  right: horizontalSpacing),
                              child: PasswordTextBox(
                                label: "Password",
                                hintText: "password",
                                screenWidth: screenWidth,
                                screenHeight: screenHeight,
                                controller: _passwordController,
                                onSubmitted: authenticate,
                              ),
                            ),
                            SizedBox(
                              height: verticalSpacing,
                            ),
                            Container(
                              height: screenWidth * 0.12,
                              width: screenWidth - horizontalSpacing * 2,
                              child: ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                      backgroundColor: AppColors.primaryColor),
                                  onPressed: isLoading ? null : authenticate,
                                  child: isLoading
                                      ? CircularProgressIndicator(
                                          color: Colors.white)
                                      : Center(
                                          child: Text(
                                            "LOGIN",
                                            style: AppTextStyles.buttonText(
                                                screenHeight,
                                                AppColors.whiteText),
                                          ),
                                        )),
                            ),
                            SizedBox(
                              height: verticalSpacing,
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Container(
                                  height: 1,
                                  width: screenWidth * 0.4,
                                  color: AppColors.paragraphText,
                                ),
                                SizedBox(
                                  width: horizontalSpacing / 2,
                                ),
                                Text(
                                  "Or",
                                  style: AppTextStyles.subtitleParagraph(
                                      screenHeight, AppColors.paragraphText),
                                ),
                                SizedBox(
                                  width: horizontalSpacing / 2,
                                ),
                                Container(
                                  height: 1,
                                  width: screenWidth * 0.4,
                                  color: AppColors.paragraphText,
                                )
                              ],
                            ),
                            SizedBox(
                              height: verticalSpacing,
                            ),
                            Platform.isIOS
                                ? Container(
                                    height: screenWidth * 0.12,
                                    width: screenWidth - horizontalSpacing * 2,
                                    child: ElevatedButton(
                                        style: ElevatedButton.styleFrom(
                                            backgroundColor: Colors.black),
                                        onPressed:
                                            isLoading ? null : authenticate,
                                        child: isLoading
                                            ? CircularProgressIndicator(
                                                color: Colors.white)
                                            : Center(
                                                child: Row(
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    Icon(
                                                      Icons.apple,
                                                      size: screenWidth * 0.08,
                                                      color:
                                                          AppColors.whiteText,
                                                    ),
                                                    SizedBox(
                                                      width:
                                                          horizontalSpacing / 2,
                                                    ),
                                                    Text(
                                                      "Sign Up with Apple",
                                                      style: AppTextStyles
                                                          .buttonText(
                                                              screenHeight,
                                                              AppColors
                                                                  .whiteText),
                                                    ),
                                                  ],
                                                ),
                                              )),
                                  )
                                : Container(),
                            Platform.isIOS
                                ? SizedBox(
                                    height: verticalSpacing,
                                  )
                                : Container(),
                            Container(
                                height: screenWidth * 0.12,
                                width: screenWidth - horizontalSpacing * 2,
                                child: OutlinedButton(
                                  onPressed: isLoading ? null : authenticate,
                                  child: isLoading
                                      ? CircularProgressIndicator(
                                          color: Colors.white)
                                      : Center(
                                          child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.center,
                                            children: [
                                              Container(
                                                  height: screenWidth * 0.1,
                                                  width: screenWidth * 0.1,
                                                  child: Image.asset(
                                                      "assets/logos/GoogleLogo.png")),
                                              SizedBox(
                                                width: horizontalSpacing / 2,
                                              ),
                                              Text(
                                                "Sign Up with Google",
                                                style: AppTextStyles.buttonText(
                                                    screenHeight, Colors.black),
                                              ),
                                            ],
                                          ),
                                        ),
                                )),
                            SizedBox(
                              height: verticalSpacing * 2,
                            ),
                            RichText(
                              text: TextSpan(
                                text: "Don't have an account? ",
                                style: AppTextStyles.subtitleParagraph(
                                    screenHeight, AppColors.paragraphText),
                                children: [
                                  TextSpan(
                                    text: "Sign Up",
                                    style: const TextStyle(
                                      color: AppColors.primaryColor,
                                      fontWeight: FontWeight.bold,
                                    ),
                                    recognizer: TapGestureRecognizer()
                                      ..onTap = () {
                                        Navigator.pushNamed(
                                            context, "/register");
                                      },
                                  ),
                                ],
                              ),
                            ),
                          ]),
                    ),
                  ],
                ),
              ),
            ),
          ]),
        ),
      ),
    );
  }

  void authenticate() async {
    String email = _emailController.text.trim();
    String password = _passwordController.text.trim();

    ScaffoldMessenger.of(context).hideCurrentSnackBar();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Please enter a valid email and password"),
          backgroundColor: AppColors.warning,
        ),
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

class StreamlineLogo extends StatelessWidget {
  const StreamlineLogo({
    super.key,
    required this.screenHeight,
    required this.color,
  });

  final double screenHeight;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Text("STREAMLINE",
        style: AppTextStyles.logoStyle(screenHeight, color));
  }
}
