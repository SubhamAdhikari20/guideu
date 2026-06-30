import 'package:flutter/material.dart';

import '../../../../app/theme/app_colors.dart';
import '../../domain/entities/booking.dart';
import 'booking_status_chip.dart';

/// A booking row in "My Bookings". Actions (pay / cancel / review) are passed in
/// by the page so this widget stays presentation-only.
class BookingCard extends StatelessWidget {
  const BookingCard({
    required this.booking,
    this.onPay,
    this.onCancel,
    this.onReview,
    super.key,
  });

  final Booking booking;
  final VoidCallback? onPay;
  final VoidCallback? onCancel;
  final VoidCallback? onReview;

  @override
  Widget build(BuildContext context) {
    final b = booking;
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    b.tourPackageTitle,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                BookingStatusChip(b.status),
              ],
            ),
            const SizedBox(height: 6),
            Row(
              children: [
                const Icon(Icons.confirmation_number_outlined,
                    size: 15, color: AppColors.textSecondary),
                const SizedBox(width: 4),
                Text(
                  b.bookingReference,
                  style: const TextStyle(
                    color: AppColors.textSecondary,
                    fontSize: 12.5,
                  ),
                ),
                const Spacer(),
                Text(
                  b.priceLabel,
                  style: const TextStyle(
                    color: AppColors.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                const Icon(Icons.calendar_today,
                    size: 14, color: AppColors.textSecondary),
                const SizedBox(width: 4),
                Text(
                  '${_d(b.startDate)} → ${_d(b.endDate)}',
                  style: const TextStyle(
                    color: AppColors.textSecondary,
                    fontSize: 12.5,
                  ),
                ),
              ],
            ),
            if (onPay != null || onCancel != null || onReview != null) ...[
              const SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  if (onCancel != null)
                    TextButton(
                      onPressed: onCancel,
                      child: const Text(
                        'Cancel',
                        style: TextStyle(color: AppColors.error),
                      ),
                    ),
                  if (onReview != null)
                    TextButton(
                      onPressed: onReview,
                      child: const Text('Leave a review'),
                    ),
                  if (onPay != null) ...[
                    const SizedBox(width: 4),
                    ElevatedButton(
                      onPressed: onPay,
                      child: const Text('Pay now'),
                    ),
                  ],
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  String _d(DateTime d) =>
      '${d.day.toString().padLeft(2, '0')}/${d.month.toString().padLeft(2, '0')}/${d.year}';
}
