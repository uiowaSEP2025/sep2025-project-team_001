import 'package:dio/dio.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobile_app/constants.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/date_input_box.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';
import 'package:mobile_app/utils/token_manager.dart';
import 'package:shared_preferences/shared_preferences.dart';

class CreateAccount extends StatefulWidget {
  const CreateAccount({super.key});

  @override
  State<CreateAccount> createState() => _CreateAccountState();
}

class _CreateAccountState extends State<CreateAccount> {
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late TextEditingController _passwordController;
  late TextEditingController _confirmPasswordController;
  late TextEditingController _birthdateController;

  bool termsAccepted = false;
  bool isLoading = false;
  bool fieldsFilled = false;
  bool isValidPassword = false;
  bool isPasswordMatch = false;
  bool isEmailValid = false;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _birthdateController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();

    super.dispose();
  }

  @override
  void initState() {
    _nameController = TextEditingController();
    _emailController = TextEditingController();
    _birthdateController = TextEditingController();
    _passwordController = TextEditingController();
    _confirmPasswordController = TextEditingController();
    super.initState();
  }

  bool validatePassword(String password) {
    if (password.length < 8) return false;
    if (!password.contains(RegExp(r'[A-Z]'))) return false;
    if (!password.contains(RegExp(r'[a-z]'))) return false;
    if (!password.contains(RegExp(r'[0-9]'))) return false;
    if (!password.contains(RegExp(r'[!@#\$&*~%^()\-\+=]'))) return false;
    return true;
  }

  bool matchPasswords(String newPassword, String confirmationPassword) {
    if (newPassword == confirmationPassword) return true;
    return false;
  }

  bool validateEmail(String email) {
    final RegExp emailRegex = RegExp(
      r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    );
      final isValid = emailRegex.hasMatch(email);
  print("Validating email: $email -> $isValid");
    return isValid;
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
      },
      child: Scaffold(
        resizeToAvoidBottomInset: true,
        backgroundColor: AppColors.backgroundColor,
        appBar: AppBar(
          elevation: 0,
          scrolledUnderElevation: 0,
          systemOverlayStyle: const SystemUiOverlayStyle(
            statusBarColor: Colors.transparent,
            statusBarIconBrightness: Brightness.dark,
            statusBarBrightness: Brightness.light,
          ),
          backgroundColor: Colors.transparent,
          title: Text("Set up your account",
              style: AppTextStyles.appBarText(screenHeight, Colors.black)),
        ),
        body: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                child: Padding(
                  padding: EdgeInsets.only(
                      top: verticalSpacing,
                      left: horizontalSpacing,
                      right: horizontalSpacing),
                  child: Column(
                    mainAxisSize: MainAxisSize.max,
                    children: [
                      Text(
                        "Please complete all fields to create your account on Streamline",
                        textAlign: TextAlign.center,
                        style: AppTextStyles.subtitleParagraph(
                            screenHeight, AppColors.paragraphText),
                      ),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      InputTextBox(
                          onChanged: () {
                            setState(() {});
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Name",
                          hintText: "Name",
                          controller: _nameController,
                          onSubmitted: onTextFieldSubmitted),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      InputTextBox(
                          onChanged: () {
                            setState(() {
                              isEmailValid =
                                  validateEmail(_emailController.text);
                            });
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Email",
                          hintText: "example@gmail.com",
                          controller: _emailController,
                          onSubmitted: onTextFieldSubmitted),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      DateInputBox(
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Birthdate",
                          hintText: "YYYY-MM-DD",
                          controller: _birthdateController),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      InputTextBox(
                          onChanged: () {
                            setState(() {
                              isValidPassword =
                                  validatePassword(_passwordController.text);
                              isPasswordMatch = matchPasswords(
                                  _passwordController.text,
                                  _confirmPasswordController.text);
                            });
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Password",
                          hintText: "********",
                          controller: _passwordController,
                          onSubmitted: onTextFieldSubmitted),
                      SizedBox(
                        height: verticalSpacing / 2,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          isValidPassword
                              ? Text(
                                  "Valid password ✅",
                                  style: AppTextStyles.smallFooters(
                                      screenHeight, AppColors.validGreen),
                                )
                              : Container(
                                  width: screenWidth - horizontalSpacing * 2,
                                  child: Text(
                                    "At least 8 characters, including uppercase, lowercase, number, and special character",
                                    style: AppTextStyles.smallFooters(
                                        screenHeight, AppColors.warning),
                                    textAlign: TextAlign.left,
                                  ),
                                ),
                        ],
                      ),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      InputTextBox(
                          onChanged: () {
                            setState(() {
                              isPasswordMatch = matchPasswords(
                                  _passwordController.text,
                                  _confirmPasswordController.text);
                            });
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Confirm Password",
                          hintText: "********",
                          controller: _confirmPasswordController,
                          onSubmitted: onTextFieldSubmitted),
                      SizedBox(
                        height: verticalSpacing / 2,
                      ),
                      _confirmPasswordController.text.isNotEmpty
                          ? Row(
                              mainAxisAlignment: MainAxisAlignment.start,
                              children: [
                                isPasswordMatch
                                    ? Text(
                                        "Passwords match ✅",
                                        style: AppTextStyles.smallFooters(
                                            screenHeight, AppColors.validGreen),
                                      )
                                    : Text(
                                        "Passwords do not match",
                                        style: AppTextStyles.smallFooters(
                                            screenHeight, AppColors.warning),
                                        textAlign: TextAlign.left,
                                      )
                              ],
                            )
                          : Container(),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
        bottomNavigationBar: Padding(
          padding: EdgeInsets.only(
              left: horizontalSpacing,
              right: horizontalSpacing,
              top: verticalSpacing / 2),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              GestureDetector(
                onTap: () {
                  setState(() {
                    termsAccepted = !termsAccepted;
                  });
                },
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    SizedBox(
                      height: 20,
                      child: Checkbox(
                        value: termsAccepted,
                        onChanged: (bool? newValue) {
                          setState(() {
                            termsAccepted = newValue ?? false;
                          });
                        },
                        activeColor: AppColors.primaryColor,
                      ),
                    ),
                    const Spacer(),
                    SizedBox(
                      width: screenWidth * 0.77,
                      child: RichText(
                        text: TextSpan(
                          text: "I agree to the ",
                          style: AppTextStyles.subtitleParagraph(
                              screenHeight, AppColors.paragraphText),
                          children: [
                            TextSpan(
                              text: "Terms and Conditions",
                              style: const TextStyle(
                                color: AppColors.primaryColor,
                                fontWeight: FontWeight.bold,
                              ),
                              recognizer: TapGestureRecognizer()
                                ..onTap = () {
                                  Navigator.pushNamed(context, "/terms");
                                },
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                height: verticalSpacing / 2,
              ),
              isLoading
                  ? const CircularProgressIndicator(
                      color: AppColors.primaryColor)
                  : ElevatedButton(
                      style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primaryColor),
                      onPressed: (_emailController.text.isEmpty ||
                              _nameController.text.isEmpty ||
                              _passwordController.text.isEmpty ||
                              _birthdateController.text.isEmpty ||
                              !termsAccepted || !isPasswordMatch || !isValidPassword)
                          ? null
                          : createAccount,
                      child: Center(
                        child: Text(
                          "Create Account",
                          style: AppTextStyles.buttonText(
                              screenHeight, AppColors.whiteText),
                        ),
                      )),
              SizedBox(
                height: verticalSpacing * 2,
              )
            ],
          ),
        ),
      ),
    );
  }

  void onTextFieldSubmitted() {}

  void createAccount() async {
    String name = _nameController.text.trim();
    String email = _emailController.text.trim();
    String password = _passwordController.text.trim();
    String confirmPassword = _confirmPasswordController.text.trim();
    final String endpoint = "${ApiConfig.baseUrl}/mobile/register/";
      ScaffoldMessenger.of(context).hideCurrentSnackBar();

    if (password != confirmPassword) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Passwords do not match"),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    if (!isEmailValid) {
      print(email);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Invalid email address"),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    setState(() => isLoading = true);

    try {
      final dio = Dio();
      final response = await dio.post(
        endpoint,
        data: {
          "name": name,
          "email": email,
          "password": password,
        },
        options: Options(headers: {"Content-Type": "application/json"}),
      );

    final tokens = response.data['tokens'];
    final accessToken = tokens['access'];
    final refreshToken = tokens['refresh'];

    await TokenManager.saveTokens(accessToken, refreshToken);

    // final prefs = await SharedPreferences.getInstance();
    // await prefs.setString('access_token', access);
    // await prefs.setString('refresh_token', refresh);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Account created successfully!"),
          backgroundColor: Colors.green,
        ),
      );

      Navigator.pop(context);
      Navigator.pushReplacementNamed(context, "/home");
    } on DioException catch (e) {
      String errorMessage = "Something went wrong";

      print("Dio error: ${e.response?.data}");
      print("Status code: ${e.response?.statusCode}");

      if (e.response?.data is Map && e.response?.data['message'] != null) {
        errorMessage = e.response!.data['message'];
      } else if (e.response?.data is Map && e.response?.data['error'] != null) {
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
}
//todo add the birtdate to the backend customer model
//todo make sure the text fields go up so that the user can see them even when the keyboard is open
