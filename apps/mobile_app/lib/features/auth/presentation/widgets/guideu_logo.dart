import 'package:flutter/material.dart';

/// The GuideU wordmark logo asset.
class GuideULogo extends StatelessWidget {
  const GuideULogo({super.key, this.height = 56});

  final double height;

  @override
  Widget build(BuildContext context) {
    return Image.asset(
      'assets/images/guideu_logo.png',
      height: height,
      fit: BoxFit.contain,
    );
  }
}
