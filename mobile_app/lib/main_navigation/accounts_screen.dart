import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';
import 'package:mobile_app/utils/token_manager.dart';
import 'package:mobile_app/utils/user_manager.dart';

class AccountScreen extends StatefulWidget {
  const AccountScreen({super.key});

  @override
  State<AccountScreen> createState() => _AccountScreenState();
}

class _AccountScreenState extends State<AccountScreen> {
  late String email = " ";
  late String name = " ";

  void _logout(BuildContext context) async {
    await TokenManager.clearTokens();
    Navigator.pushReplacementNamed(context, "/"); // back to login
  }

  @override
  void initState() {
    loadEmail();
    super.initState();
  }

  void loadEmail() async {
    final retrievedEmail = await UserManager.getEmail();
    final retrievedName = await UserManager.getName();
    setState(() {
      email = retrievedEmail ?? '';
      name = retrievedName ?? '';
    });
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    double horizontalSpacing = screenWidth * 0.05;
    double verticalSpacing = screenHeight * 0.025;

    return Scaffold(
      appBar: AppBar(
          title: Text("Account",
              style: AppTextStyles.appBarText(screenHeight, Colors.black))),
      body: Padding(
        padding: EdgeInsets.all(horizontalSpacing),
        child: Column(
          children: [
            ListTile(
              leading: const Icon(Icons.person),
              title: Text("Name"),
              subtitle: name != null ? Text(name) : null,
            ),
             SizedBox(height: verticalSpacing/2),
            ListTile(
              leading: const Icon(Icons.email),
              title: const Text("Email"),
              subtitle: email != null ? Text(email) : null,
            ),
            SizedBox(height: verticalSpacing/2),
            ElevatedButton.icon(
              onPressed: () => _logout(context),
              icon: const Icon(Icons.logout, color: Colors.white,),
              label: Text(
                "Logout",
                style:
                    AppTextStyles.buttonText(screenHeight, AppColors.whiteText),
              ),
              style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryColor),
            )
          ],
        ),
      ),
    );
  }
}
