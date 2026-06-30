import 'package:flutter/material.dart';

import '../../../../app/theme/app_colors.dart';
import '../../domain/entities/booking.dart';

/// Coloured pill showing a booking's status.
class BookingStatusChip extends StatelessWidget {
  const BookingStatusChip(this.status, {super.key});

  final BookingStatus status;

  Color get _color {
    switch (status) {
      case BookingStatus.pending:
        return AppColors.gold;
      case BookingStatus.confirmed:
      case BookingStatus.active:
        return AppColors.primary;
      case BookingStatus.completed:
        return AppColors.success;
      case BookingStatus.cancelled:
        return AppColors.error;
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
        status.label,
        style: TextStyle(
          color: _color,
          fontSize: 12,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
