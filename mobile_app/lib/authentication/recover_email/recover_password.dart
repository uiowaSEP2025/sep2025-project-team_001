import 'package:flutter/material.dart';
import 'package:mobile_app/authentication/recover_email/widgets/enter_new_password.dart';
import 'package:mobile_app/authentication/recover_email/widgets/enter_recovery_code.dart';
import 'package:mobile_app/authentication/recover_email/widgets/enter_recovery_email.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';

class RecoverPasswordScreen extends StatefulWidget {
  const RecoverPasswordScreen({super.key});

  @override
  State<RecoverPasswordScreen> createState() => _RecoverPasswordScreenState();
}

class _RecoverPasswordScreenState extends State<RecoverPasswordScreen> {
  final PageController _pageController = PageController();
  int _currentStep = 0;
  String email = "";

  void goToNextStep() {
    if (_currentStep < 2) {
      setState(() {
        _currentStep++;
      });
      _pageController.animateToPage(
        _currentStep,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  void goToPreviousStep() {
    if (_currentStep > 0) {
      setState(() {
        _currentStep--;
      });
      _pageController.animateToPage(
        _currentStep,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    } else {
      Navigator.pop(context);
    }
  }

  void setEmail(String newEmail) {
    setState(() {
      email = newEmail;
    });
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return GestureDetector(
      onTap: () {
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        FocusScope.of(context).unfocus();
      },
      child: PopScope(
        canPop: _currentStep == 0,
        onPopInvoked: (didPop) {
          if (!didPop && _currentStep > 0) {
            if (_currentStep > 0) {
              setState(() {
                _currentStep--;
              });
              _pageController.animateToPage(
                _currentStep,
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              );
            } else {
              Navigator.pop(context);
            }
          }
        },
        child: Scaffold(
          backgroundColor: AppColors.backgroundColor,
          appBar: AppBar(
            title: Text('Recover Password',
                style: AppTextStyles.appBarText(screenHeight, Colors.black)),
          ),
          body: PageView(
            physics: const NeverScrollableScrollPhysics(),
            controller: _pageController,
            children: [
              EnterRecoveryEmail(
                  onNext: goToNextStep,
                  enterEmail: setEmail,
                  enteredEmail: email),
              EnterRecoveryCode(onNext: goToNextStep, enteredEmail: email),
              EnterNewPassword(
                  onNext: () => Navigator.pop(context), enteredEmail: email),
            ],
          ),
        ),
      ),
    );
  }
}
