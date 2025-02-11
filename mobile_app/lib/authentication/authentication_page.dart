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
        backgroundColor: AppColors.backgroundColor,
        appBar: AppBar(
          leading: Text('app logo placeholder'),
        ),
        body: Container(
          width: screenWidth,
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.center, children: [
            SizedBox(
              height: screenWidth * 0.2,
            ),
            Text(
              "Hello!",
              style: AppTextStyles.bigBoldLetters(
                  screenHeight, AppColors.whiteText),
            ),
            SizedBox(
              height: spacing,
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
              height: spacing*2,
            ),
            
            Padding(
              padding: EdgeInsets.only(left: spacing, right: spacing),
              child: InputTextBox(label: "Email", hintText: "johndoe@gmail.com",screenWidth: screenWidth, screenHeight: screenHeight,),
            ),
            SizedBox(
              height: spacing,
            ),
            Padding(
              padding: EdgeInsets.only(left: spacing, right: spacing),
              child: InputTextBox(label: "Password", hintText: "********",screenWidth: screenWidth, screenHeight: screenHeight,),
            ),
          ]),
        ));
  }
}

class InputTextBox extends StatelessWidget {
  const InputTextBox({
    super.key,
    required this.screenWidth,
    required this.screenHeight,
    required this.label,
    required this.hintText
  });

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
                Text(label,style: AppTextStyles.textFieldLabel(screenHeight, AppColors.whiteText),),
              ],
            ),
            
        Container(
          height: screenWidth*0.12,
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
