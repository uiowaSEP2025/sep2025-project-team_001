import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';

class EnterNewPassword extends StatefulWidget {
  final VoidCallback onNext;
  final String enteredEmail;

  const EnterNewPassword(
      {super.key, required this.onNext, required this.enteredEmail});

  @override
  State<EnterNewPassword> createState() => _EnterNewPasswordState();
}

class _EnterNewPasswordState extends State<EnterNewPassword> {
  late TextEditingController _newPassword;
  late TextEditingController _confirmedPassword;
  bool isValidPassword = false;
  bool isPasswordMatch = false;

  bool isLoading = false;

  @override
  void initState() {
    _newPassword = TextEditingController();
    _confirmedPassword = TextEditingController();
    super.initState();
  }

  @override
  void dispose() {
    _newPassword.dispose();
    _confirmedPassword.dispose();
    super.dispose();
  }

  void setNewPassword() {
    setState(() {
      isLoading = true;
    });

    sendPasswordToApi();

    setState(() {
      isLoading = true;
    });

    //todo pop if password was successfully set 
    Navigator.pop(context);
  }

  void sendPasswordToApi() {
    //todo send new password to api to validate it
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

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Padding(
      padding: EdgeInsets.only(
          left: horizontalSpacing,
          right: horizontalSpacing,
          top: verticalSpacing),
      child: Column(
        children: [
          Text(
            "Please enter a new password for your account",
            textAlign: TextAlign.center,
            style: AppTextStyles.subtitleParagraph(
                screenHeight, AppColors.paragraphText),
          ),
          SizedBox(
            height: verticalSpacing,
          ),
          InputTextBox(
              onChanged: () {
                setState(() {
                  isValidPassword = validatePassword(_newPassword.text);
                  isPasswordMatch = matchPasswords(
                      _newPassword.text, _confirmedPassword.text);
                });
              },
              screenWidth: screenWidth,
              screenHeight: screenHeight,
              label: "New Password",
              hintText: "New Password",
              controller: _newPassword,
              onSubmitted: setNewPassword),
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
                      _newPassword.text, _confirmedPassword.text);
                });
              },
              screenWidth: screenWidth,
              screenHeight: screenHeight,
              label: "Confirm Password",
              hintText: "Confirm Password",
              controller: _confirmedPassword,
              onSubmitted: setNewPassword),
          SizedBox(
            height: verticalSpacing / 2,
          ),
          _confirmedPassword.text.isNotEmpty
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
          Spacer(),
          isLoading
              ? const CircularProgressIndicator(color: Colors.white)
              : ElevatedButton(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryColor),
                  onPressed: (_newPassword.text.isEmpty ||
                          _confirmedPassword.text.isEmpty ||
                          !isValidPassword ||
                          !isPasswordMatch)
                      ? null
                      : setNewPassword,
                  child: Center(
                    child: Text(
                      "SET PASSWORD",
                      style: AppTextStyles.buttonText(
                          screenHeight, AppColors.whiteText),
                    ),
                  )),
          SizedBox(
            height: verticalSpacing * 2,
          )
        ],
      ),
    );
  }
}
