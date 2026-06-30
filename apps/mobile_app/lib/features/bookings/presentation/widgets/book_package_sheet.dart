import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme/app_colors.dart';
import '../../domain/entities/tour_package.dart';
import '../../domain/usecases/create_booking_usecase.dart';
import '../providers/booking_providers.dart';

/// Opens the "Book package" sheet. Returns `true` if a booking was created.
Future<bool?> showBookPackageSheet(BuildContext context, TourPackage package) {
  return showModalBottomSheet<bool>(
    context: context,
    isScrollControlled: true,
    backgroundColor: AppColors.surface,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (context) => Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
      ),
      child: _BookPackageSheet(package: package),
    ),
  );
}

class _BookPackageSheet extends ConsumerStatefulWidget {
  const _BookPackageSheet({required this.package});

  final TourPackage package;

  @override
  ConsumerState<_BookPackageSheet> createState() => _BookPackageSheetState();
}

class _BookPackageSheetState extends ConsumerState<_BookPackageSheet> {
  final _notesController = TextEditingController();
  DateTime? _startDate;
  bool _submitting = false;

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  DateTime get _endDate =>
      (_startDate ?? DateTime.now()).add(Duration(days: widget.package.durationDays));

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: _startDate ?? now.add(const Duration(days: 1)),
      firstDate: now,
      lastDate: now.add(const Duration(days: 365)),
    );
    if (picked != null) setState(() => _startDate = picked);
  }

  Future<void> _confirm() async {
    if (_startDate == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please choose a start date.')),
      );
      return;
    }
    setState(() => _submitting = true);
    final (failure, booking) = await ref.read(createBookingUseCaseProvider).call(
          CreateBookingParams(
            packageId: widget.package.id,
            startDate: _startDate!,
            endDate: _endDate,
            notes: _notesController.text.trim(),
          ),
        );
    if (!mounted) return;
    setState(() => _submitting = false);
    if (booking != null) {
      ref.invalidate(myBookingsProvider);
      Navigator.of(context).pop(true);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(failure?.message ?? 'Could not book.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final p = widget.package;
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text(
                'Book this package',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const Spacer(),
              IconButton(
                icon: const Icon(Icons.close),
                onPressed: () => Navigator.of(context).pop(false),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(p.title, style: const TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 2),
          Text(
            '${p.durationLabel}  •  ${p.priceLabel}',
            style: const TextStyle(color: AppColors.textSecondary),
          ),
          const SizedBox(height: 16),
          InkWell(
            onTap: _pickDate,
            borderRadius: BorderRadius.circular(12),
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.inputFill,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(Icons.calendar_today,
                      size: 18, color: AppColors.primary),
                  const SizedBox(width: 10),
                  Text(
                    _startDate == null
                        ? 'Choose start date'
                        : 'Start: ${_dateLabel(_startDate!)}  →  ${_dateLabel(_endDate)}',
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _notesController,
            maxLines: 2,
            decoration: const InputDecoration(
              hintText: 'Any notes for the trip (optional)',
            ),
          ),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _submitting ? null : _confirm,
              child: _submitting
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : Text('Confirm booking • ${p.priceLabel}'),
            ),
          ),
        ],
      ),
    );
  }

  String _dateLabel(DateTime d) =>
      '${d.day.toString().padLeft(2, '0')}/'
      '${d.month.toString().padLeft(2, '0')}/${d.year}';
}
