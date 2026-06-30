import 'package:flutter/material.dart';

import '../../../../app/theme/app_colors.dart';

/// Small coloured pill showing a trek's difficulty, matching the Explore
/// prototype (green = easy, amber = moderate, red = hard).
class DifficultyBadge extends StatelessWidget {
  const DifficultyBadge(this.difficulty, {super.key});

  final String difficulty;

  Color get _color {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return AppColors.success;
      case 'moderate':
        return AppColors.gold;
      case 'hard':
      case 'very hard':
        return AppColors.error;
      default:
        return AppColors.textSecondary;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: _color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        difficulty,
        style: TextStyle(
          color: _color,
          fontSize: 12,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
