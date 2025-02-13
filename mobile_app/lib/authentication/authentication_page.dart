import 'package:flutter/material.dart';
import 'package:mobile_app/design/app_colors.dart';
import 'package:mobile_app/design/app_text_styles.dart';

class AuthenticationPage extends StatefulWidget {
  const AuthenticationPage({super.key});

  @override
  State<AuthenticationPage> createState() => _AuthenticationPageState();
}

class _AuthenticationPageState extends State<AuthenticationPage> {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double spacing = screenWidth * 0.05;

    return Scaffold(
        body: GestureDetector(
      onTap: () {
        FocusManager.instance.primaryFocus?.unfocus();
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
              height: screenWidth * 0.2,
            ),
            Container(
              width: screenWidth * 0.7,
              child: Image.asset("assets/images/StreamlineLogo.png"),
            ),
            SizedBox(
              height: spacing / 2,
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
              height: spacing,
            ),
            Padding(
              padding: EdgeInsets.only(left: spacing, right: spacing),
              child: InputTextBox(
                label: "Email",
                hintText: "johndoe@gmail.com",
                screenWidth: screenWidth,
                screenHeight: screenHeight,
              ),
            ),
            SizedBox(
              height: spacing,
            ),
            Padding(
              padding: EdgeInsets.only(left: spacing, right: spacing),
              child: InputTextBox(
                label: "Password",
                hintText: "********",
                screenWidth: screenWidth,
                screenHeight: screenHeight,
              ),
            ),
            SizedBox(
              height: spacing * 2,
            ),
            ElevatedButton(
                onPressed: authenticate(),
                child: Container(
                  height: screenWidth * 0.12,
                  width: screenWidth - spacing * 2,
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10),
                      color: AppColors.primaryColor),
                  child: Center(
                    child: Text(
                      "SIGN UP/LOGIN",
                      style: AppTextStyles.buttonText(
                          screenHeight, AppColors.whiteText),
                    ),
                  ),
                )),
            SizedBox(
              height: spacing,
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
                  width: spacing / 2,
                ),
                Text(
                  "Or continue with",
                  style: AppTextStyles.subtitleParagraph(
                      screenHeight, AppColors.whiteText),
                ),
                SizedBox(
                  width: spacing / 2,
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
              height: spacing * 2,
            ),
            Row(
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
                  width: spacing * 2,
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
                  child: Icon(Icons.apple, size: screenWidth*0.11, color: AppColors.whiteText,) , //todo check what platform is running and dont show if it is running on an android 
                ),
              ],
            )
          ]),
        ),
      ),
    ));
  }

  authenticate() {}

  closeKeyboard() {}
}

class InputTextBox extends StatelessWidget {
  const InputTextBox(
      {super.key,
      required this.screenWidth,
      required this.screenHeight,
      required this.label,
      required this.hintText});

  final double screenWidth;
  final double screenHeight;
  final String label;
  final String hintText;

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
