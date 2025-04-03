import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';
import 'package:mobile_app/utils/token_manager.dart';
import 'package:mobile_app/utils/user_manager.dart';
import 'dart:ui';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mobile_app/design/widgets/user_input/password_text_box.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthenticationPage extends StatefulWidget {
  final Dio? dio;
  const AuthenticationPage({super.key, this.dio});

  @override
  State<AuthenticationPage> createState() => _AuthenticationPageState();
}

class _AuthenticationPageState extends State<AuthenticationPage> {
  late TextEditingController _emailController;
  late TextEditingController _passwordController;
  String email = "";
  String password = "";
  bool isLoading = false;

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

  void signInWithApple() async {
    print("sign in with apple");
  }

  void signInWithGoogle() async {
    print("sign in with google");
  }

  void authenticate() async {
    final String email = _emailController.text.trim();
    UserManager.saveEmail(email);
    final String password = _passwordController.text.trim();
    const String endpoint = "${ApiConfig.baseUrl}/mobile/login/";
    ScaffoldMessenger.of(context).hideCurrentSnackBar();

    print(email);
    print(password);
    print(endpoint);

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Please enter email and password"),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    setState(() => isLoading = true);

    try {
      final dio = widget.dio ?? Dio();

      final response = await dio.post(
        endpoint,
        data: {
          "username": email,
          "password": password,
        },
        options: Options(headers: {"Content-Type": "application/json"}),
      );

      final tokens = response.data['tokens'];
      final accessToken = tokens['access'];
      final refreshToken = tokens['refresh'];

      final userId = response.data['customer_id'];


      print(response);
      
      final userName = response.data['name'];

      await UserManager.saveUser(userId);

      print(userId);
      print(userName);

      await TokenManager.saveTokens(accessToken, refreshToken);
      await UserManager.saveName(userName);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Login successful!"),
          backgroundColor: Colors.green,
        ),
      );
      print("about to navigate to home");
      Navigator.pushReplacementNamed(context, "/home");
    } on DioException catch (e) {
      String errorMessage = "Your password is incorrect";

      print("Login error: ${e.response?.data}");
      print("Status code: ${e.response?.statusCode}");

      if (e.response?.data is Map && e.response?.data['error'] != null) {
        errorMessage = e.response!.data['error'];
      } else if (e.response?.data is Map) {
        errorMessage = e.response!.data.toString();
      }

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(errorMessage),
          backgroundColor: AppColors.warning,
        ),
      );
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return AnnotatedRegion<SystemUiOverlayStyle>(
      value: const SystemUiOverlayStyle(
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
                physics: const AlwaysScrollableScrollPhysics(),
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
                                onChanged: () {
                                  setState() {}
                                },
                                label: "Email",
                                hintText: "example@gmail.com",
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
                              height: verticalSpacing * 0.4,
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.end,
                              children: [
                                GestureDetector(
                                    onTap: () {
                                      Navigator.pushNamed(
                                          context, "/recover_password");
                                    },
                                    child: Text(
                                      "Forgot Password?",
                                      style: AppTextStyles.smallFooters(
                                          screenHeight,
                                          AppColors.paragraphText),
                                    )),
                                SizedBox(
                                  width: horizontalSpacing,
                                )
                              ],
                            ),
                            SizedBox(
                              height: verticalSpacing,
                            ),
                            SizedBox(
                              height: screenWidth * 0.12,
                              width: screenWidth - horizontalSpacing * 2,
                              child: ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                      backgroundColor: AppColors.primaryColor),
                                  onPressed: isLoading ? null : authenticate,
                                  child: isLoading
                                      ? const CircularProgressIndicator(
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
                            // Platform.isIOS
                            defaultTargetPlatform == TargetPlatform.iOS
                                ? SizedBox(
                                    height: screenWidth * 0.12,
                                    width: screenWidth - horizontalSpacing * 2,
                                    child: ElevatedButton(
                                        style: ElevatedButton.styleFrom(
                                            backgroundColor: Colors.black),
                                        onPressed:
                                            isLoading ? null : signInWithApple,
                                        child: isLoading
                                            ? const CircularProgressIndicator(
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
                                                      "Sign In with Apple",
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
                            defaultTargetPlatform == TargetPlatform.iOS
                                ? SizedBox(
                                    height: verticalSpacing,
                                  )
                                : Container(),
                            SizedBox(
                                height: screenWidth * 0.12,
                                width: screenWidth - horizontalSpacing * 2,
                                child: OutlinedButton(
                                  onPressed:
                                      isLoading ? null : signInWithGoogle,
                                  child: isLoading
                                      ? const CircularProgressIndicator(
                                          color: Colors.white)
                                      : Center(
                                          child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.center,
                                            children: [
                                              SizedBox(
                                                  height: screenWidth * 0.1,
                                                  width: screenWidth * 0.1,
                                                  child: Image.asset(
                                                      "assets/logos/GoogleLogo.png")),
                                              SizedBox(
                                                width: horizontalSpacing / 2,
                                              ),
                                              Text(
                                                "Sign In with Google",
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
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  "Don't have an account? ",
                                  style: AppTextStyles.subtitleParagraph(
                                      screenHeight, AppColors.paragraphText),
                                ),
                                GestureDetector(
                                  key: const Key('signUpButton'),
                                  onTap: () {
                                    Navigator.pushNamed(context, "/register");
                                  },
                                  child: Text(
                                    "Sign Up",
                                    style: AppTextStyles.buttonText(
                                        screenHeight, AppColors.primaryColor),
                                  ),
                                )
                              ],
                            )
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
