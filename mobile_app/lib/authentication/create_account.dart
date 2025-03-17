import 'package:flutter/cupertino.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/design/app_colors.dart';
import 'package:mobile_app/design/app_text_styles.dart';
import 'package:mobile_app/design/widgets/input_text_box.dart';

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

  bool termsAccepted = false;
  bool isLoading = false;
  bool fieldsFilled = false;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    _nameController = TextEditingController();
    _emailController = TextEditingController();
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
        appBar: AppBar(
          title: Text("Set up your account",
              style: AppTextStyles.appBarText(screenHeight, Colors.black)),
        ),
        body: Padding(
          padding: EdgeInsets.only(
              top: verticalSpacing,
              left: horizontalSpacing,
              right: horizontalSpacing),
          child: Column(
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
                  screenWidth: screenWidth,
                  screenHeight: screenHeight,
                  label: "Name",
                  hintText: "Name",
                  controller: _nameController,
                  onSubmitted: onTextFieldSubmitted),
              InputTextBox(
                  screenWidth: screenWidth,
                  screenHeight: screenHeight,
                  label: "Email",
                  hintText: "Email",
                  controller: _emailController,
                  onSubmitted: onTextFieldSubmitted),
              InputTextBox(
                  screenWidth: screenWidth,
                  screenHeight: screenHeight,
                  label: "Password",
                  hintText: "********",
                  controller: _passwordController,
                  onSubmitted: onTextFieldSubmitted),
              InputTextBox(
                  screenWidth: screenWidth,
                  screenHeight: screenHeight,
                  label: "Confirm Password",
                  hintText: "********",
                  controller: _nameController,
                  onSubmitted: onTextFieldSubmitted),
              Spacer(),
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
                    Container(
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
                    Container(
                      width: screenWidth * 0.77,
                      child: RichText(
                        text: TextSpan(
                          text: "I agree to the ",
                          style: AppTextStyles.subtitleParagraph(screenHeight, AppColors.paragraphText),
                          children: [
                            TextSpan(
                              text: "Terms of Use",
                              style: TextStyle(
                                color: AppColors.primaryColor,
                                fontWeight: FontWeight.bold,
                              ),
                              recognizer: TapGestureRecognizer()
                                ..onTap = () {
                                  Navigator.pushNamed(context, "/terms");
                                },
                            ),
                            TextSpan(text: " and "),
                            TextSpan(
                              text: "Privacy Policy",
                              style: TextStyle(
                                color: AppColors.primaryColor,
                                fontWeight: FontWeight.bold,
                              ),
                              recognizer: TapGestureRecognizer()
                                ..onTap = () {
                                  Navigator.pushNamed(context, "/privacy");
                                },
                            ),
                          ],
                        ),
                      ),
                    ),
                  
                  ],
                ),
              ),
              SizedBox(height: verticalSpacing,),
              ElevatedButton(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryColor),
                  onPressed: isLoading ? null : createAccount,
                  child: isLoading
                      ? CircularProgressIndicator(color: Colors.white)
                      : Center(
                          child: Text(
                            "Create Account",
                            style: AppTextStyles.buttonText(
                                screenHeight, AppColors.whiteText),
                          ),
                        )),
                        SizedBox(height: verticalSpacing*2,)
            ],
          ),
        ),
      ),
    );
  }

  void onTextFieldSubmitted() {}

  void createAccount() {}
}
