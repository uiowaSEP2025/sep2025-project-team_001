import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/design/widgets/user_input/input_text_box.dart';

class EnterRecoveryEmail extends StatefulWidget {
  final VoidCallback onNext;

  const EnterRecoveryEmail({super.key, required this.onNext});

  @override
  State<EnterRecoveryEmail> createState() => _EnterRecoveryEmailState();
}

class _EnterRecoveryEmailState extends State<EnterRecoveryEmail> {
  late TextEditingController _recoveryEmailController;
  bool isLoading = false;

  @override
  void dispose() {
    _recoveryEmailController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    _recoveryEmailController = TextEditingController();
    super.initState();
  }

  void enterRecoveryEmail() async {
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
            "Please enter the email associated to your account",
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
              label: "",
              hintText: "Email",
              controller: _recoveryEmailController,
              onSubmitted: enterRecoveryEmail),
          Spacer(),
          isLoading
              ? const CircularProgressIndicator(color: Colors.white)
              : ElevatedButton(
                  style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primaryColor),
                  onPressed: (_recoveryEmailController.text.isEmpty)
                      ? null
                      : enterRecoveryEmail,
                  child: Center(
                    child: Text(
                      "RECOVER PASSWORD",
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
