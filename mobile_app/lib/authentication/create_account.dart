import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/date_input_box.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';

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
        resizeToAvoidBottomInset: false,
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
                            setState() {}
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Email",
                          hintText: "Email",
                          controller: _emailController,
                          onSubmitted: onTextFieldSubmitted),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      DateInputBox(
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Birthdate",
                          hintText: "Birthdate",
                          controller: _birthdateController),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      InputTextBox(
                          onChanged: () {
                            setState() {}
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Password",
                          hintText: "********",
                          controller: _passwordController,
                          onSubmitted: onTextFieldSubmitted),
                      SizedBox(
                        height: verticalSpacing,
                      ),
                      InputTextBox(
                          onChanged: () {
                            setState() {}
                          },
                          screenWidth: screenWidth,
                          screenHeight: screenHeight,
                          label: "Confirm Password",
                          hintText: "********",
                          controller: _confirmPasswordController,
                          onSubmitted: onTextFieldSubmitted),
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
              top: verticalSpacing),
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
                height: verticalSpacing,
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
                              !termsAccepted)
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

  void createAccount() {}
}
