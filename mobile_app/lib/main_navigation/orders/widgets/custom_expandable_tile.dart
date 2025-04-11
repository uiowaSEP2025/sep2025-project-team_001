import 'package:flutter/material.dart';

class CustomExpandableTile extends StatefulWidget {
  final Widget collapsedChild;
  final Widget expandedChild;

  const CustomExpandableTile({
    required this.collapsedChild,
    required this.expandedChild,
    super.key,
  });

  @override
  State<CustomExpandableTile> createState() => _CustomExpandableTileState();
}

class _CustomExpandableTileState extends State<CustomExpandableTile> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        GestureDetector(
          onTap: () => setState(() => _expanded = !_expanded),
          child: widget.collapsedChild,
        ),
        AnimatedCrossFade(
          firstChild: const SizedBox.shrink(),
          secondChild: widget.expandedChild,
          crossFadeState:
              _expanded ? CrossFadeState.showSecond : CrossFadeState.showFirst,
          duration: const Duration(milliseconds: 200),
        ),
      ],
    );
  }
}
