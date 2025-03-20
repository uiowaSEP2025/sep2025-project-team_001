import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/four_digit_code_field.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';

class EnterRecoveryCode extends StatefulWidget {
  final VoidCallback onNext;
  final String enteredEmail;

  EnterRecoveryCode(
      {super.key, required this.onNext, required this.enteredEmail});

  @override
  State<EnterRecoveryCode> createState() => _EnterRecoveryCodeState();
}

class _EnterRecoveryCodeState extends State<EnterRecoveryCode> {
  bool isLoading = false;
  bool enteredCode = false;
  bool invalidCode = false;
  String code = "";

  void sendCodeApiCall() {
    //todo call api to send code and validate it
    if (code == "0000") {
      invalidCode = true;
    } else {
      invalidCode = false;
    }
  }

  void validateCode() async {
    setState(() {
      isLoading = true;
    });

//call api to send email
    sendCodeApiCall();

    if (!invalidCode) {
      widget.onNext();
    }

    setState(() {
      isLoading = false;
    });
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
            "We sent a validation code to ",
            textAlign: TextAlign.center,
            style: AppTextStyles.subtitleParagraph(
                screenHeight, AppColors.paragraphText),
          ),
          Text(
            widget.enteredEmail,
            textAlign: TextAlign.center,
            style: AppTextStyles.subtitleParagraph(
                screenHeight, AppColors.primaryColor),
          ),
          SizedBox(
            height: verticalSpacing,
          ),
          FourDigitCodeField(
            screenHeight: screenHeight,
            screenWidth: screenWidth,
            onChanged: (code) {
              setState(() {
                this.code = code;
                if (code.length == 4) {
                  enteredCode = true;
                  submitCode();
                } else {
                  enteredCode = false;
                }
              });
            },
          ),
          SizedBox(
            height: verticalSpacing / 2,
          ),
          invalidCode
              ? Text("Invalid code",
                  style: AppTextStyles.subtitleParagraph(
                      screenHeight, AppColors.warning))
              : Container(),
          Spacer(),
          isLoading
              ? const CircularProgressIndicator(color: Colors.white)
              : ElevatedButton(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryColor),
                  onPressed: (enteredCode) ? validateCode : null,
                  child: Center(
                    child: Text(
                      "VALIDATE CODE",
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

  void submitCode() {}
}
