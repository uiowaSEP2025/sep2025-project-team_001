import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobile_app/design/app_colors.dart';
import 'package:mobile_app/design/app_text_styles.dart';

class TermsAndConditionsScreen extends StatelessWidget {
  const TermsAndConditionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Scaffold(
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
        title: Text("Terms and Conditions",
            style: AppTextStyles.appBarText(screenHeight, Colors.black)),
      ),
      body: SingleChildScrollView(
          child: Padding(
        padding: EdgeInsets.only(
            left: horizontalSpacing,
            right: horizontalSpacing,
            top: verticalSpacing),
        child: RichText(
          text: TextSpan(
            style: AppTextStyles.subtitleParagraph(
                screenHeight, AppColors.paragraphText),
            children: [
              TextSpan(
                  text: "1. Acceptance of Terms\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "By accessing or using our App, you confirm that you have read, understood, and agree to be bound by these Terms. If you do not agree with any part of these Terms, please do not use the App.\n\n\n",
              ),
              TextSpan(
                  text: "2. Eligibility\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "You must be 21 years or older (or the legal drinking age in your jurisdiction) to use the App. By using the App, you represent and warrant that you have the legal capacity to enter into these Terms. The app only allows for you to order if you are inside the bar/restaurant premises where you will be required to show an official ID to validate your age\n\n\n",
              ),
              TextSpan(
                  text: "3. Use of the App\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "The App allows users to browse bars, book reservations, access promotions, and engage with bar-related content. You agree to use the App only for lawful purposes and in compliance with all applicable laws and regulations.\n\n\n",
              ),
              TextSpan(
                  text: "4. Account Registration\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "Some features may require you to create an account. You must provide accurate and complete information when registering. You are responsible for maintaining the confidentiality of your account and password.\n\n\n",
              ),
              TextSpan(
                  text: "5. Bar Listings and Promotions\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "The App provides information about bars, including their location, events, and promotions. We do not own or operate the bars listed in the App and are not responsible for their services or policies. Promotions and discounts offered through the App are subject to the terms set by each bar.\n\n\n",
              ),
              TextSpan(
                  text: "6. User Conduct\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "When using the App, you agree NOT to:\n- Impersonate any person or entity.\n- Post false or misleading information.\n- Engage in harassment, abuse, or hate speech.\n- Attempt to hack, modify, or interfere with the App’s security or performance.\n\n\n",
              ),
              TextSpan(
                  text: "7. Payments & Refunds\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "We are not responsible for refunds related to bar reservations or purchases made outside the App.\n\n\n",
              ),
              TextSpan(
                  text: "8. Privacy Policy\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "We collect and use your data only for the purpose of the app.\n\n\n",
              ),
              TextSpan(
                  text: "9. Limitation of Liability\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "The App is provided 'as is' without any warranties. We are not liable for any damages arising from your use of the App, including but not limited to bar experiences, bookings, or promotions. Bars listed on the App are responsible for their own services and policies.\n\n\n",
              ),
              TextSpan(
                  text: "10. Termination\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text:
                    "We reserve the right to suspend or terminate your account if you violate these Terms. You may stop using the App at any time.\n\n\n",
              ),
              TextSpan(
                  text: "11. Changes to Terms\n\n",
                  style:
                      AppTextStyles.textFieldLabel(screenHeight, Colors.black)),
              const TextSpan(
                text: "We may update these Terms at any time.\n\n\n",
              ),
            ],
          ),
        ),
      )),
    );
  }
}
