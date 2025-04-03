import 'package:flutter/material.dart';
import 'package:mobile_app/design/styling/app_colors.dart';
import 'package:mobile_app/design/styling/app_text_styles.dart';

class DateInputBox extends StatefulWidget {
  final double screenWidth;
  final double screenHeight;
  final String label;
  final String hintText;
  final TextEditingController controller;

  const DateInputBox(
      {super.key,
      required this.screenWidth,
      required this.screenHeight,
      required this.label,
      required this.hintText,
      required this.controller});

  @override
  State<DateInputBox> createState() => _DateInputBoxState();
}

class _DateInputBoxState extends State<DateInputBox> {
  Future<void> _selectDate(BuildContext context) async {
    DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime(2000, 1, 1),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
      builder: (BuildContext context, Widget? child) {
        return Theme(
          data: ThemeData(
            colorScheme: const ColorScheme.light(
              primary: AppColors.primaryColor,
              onPrimary: Colors.white,
              onSurface: Colors.black,
            ),
            dialogBackgroundColor: Colors.white,
          ),
          child: child!,
        );
      },
    );

    if (pickedDate != null) {
      setState(() {
        widget.controller.text =
            "${pickedDate.year}-${pickedDate.month.toString().padLeft(2, '0')}-${pickedDate.day.toString().padLeft(2, '0')}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Text(
              widget.label,
              style: AppTextStyles.textFieldLabel(
                  widget.screenHeight, AppColors.paragraphText),
            ),
          ],
        ),
        GestureDetector(
          onTap: () => _selectDate(context),
          child: Container(
            height: widget.screenWidth * 0.12,
            decoration: BoxDecoration(
              color: AppColors.whiteText,
              border: Border.all(color: Colors.black),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Row(
              children: [
                Expanded(
                  child: Padding(
                    padding: EdgeInsets.only(left: widget.screenWidth * 0.025),
                    child: Text(
                        widget.controller.text.isEmpty
                            ? widget.hintText
                            : widget.controller.text,
                        style: AppTextStyles.subtitleParagraph(
                          widget.screenHeight,
                          widget.controller.text.isEmpty
                              ? Colors.grey
                              : Colors.black,
                        )),
                  ),
                ),
                const Icon(Icons.calendar_today, color: Colors.black),
                SizedBox(
                  width: widget.screenWidth * 0.025,
                )
              ],
            ),
          ),
        ),
      ],
    );
  }
}
