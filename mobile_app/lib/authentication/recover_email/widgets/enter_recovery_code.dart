import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/four_digit_code_field.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';

class EnterRecoveryCode extends StatefulWidget {
  final VoidCallback onNext;

  EnterRecoveryCode({super.key, required this.onNext});

  @override
  State<EnterRecoveryCode> createState() => _EnterRecoveryCodeState();
}

class _EnterRecoveryCodeState extends State<EnterRecoveryCode> {
  bool isLoading = false;
  bool enteredCode = true;
  String code = "";

  void validateCode() async {
    setState(() {
      isLoading = true;
    });

//call api to send email

    widget.onNext();

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
            "We send the code to ",
            textAlign: TextAlign.center,
            style: AppTextStyles.subtitleParagraph(
                screenHeight, AppColors.paragraphText),
          ),
          SizedBox(
            height: verticalSpacing,
          ),
          FourDigitCodeField(
            onCompleted: (code) {
              // setState(() {
              //    this.code = code;
              // print("Entered Code: $code");
              // });
             
            },
          ),
          Spacer(),
          isLoading
              ? const CircularProgressIndicator(color: Colors.white)
              : ElevatedButton(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryColor),
                  onPressed: (code == "") ? null : validateCode,
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
}
