import 'package:flutter/material.dart';

import '../../../../app/theme/app_colors.dart';
import '../../domain/entities/destination.dart';

/// Opens the "Destination Details" bottom sheet for a [Destination], matching
/// the prototype: hero image, summary, a 2x2 fact grid and the permit list.
/// [onFindGuide] is invoked when the user taps the call-to-action.
Future<void> showDestinationDetailSheet(
  BuildContext context,
  Destination destination, {
  VoidCallback? onFindGuide,
}) {
  return showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: AppColors.surface,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (context) => _DestinationDetailSheet(
      destination: destination,
      onFindGuide: onFindGuide,
    ),
  );
}

class _DestinationDetailSheet extends StatelessWidget {
  const _DestinationDetailSheet({required this.destination, this.onFindGuide});

  final Destination destination;
  final VoidCallback? onFindGuide;

  @override
  Widget build(BuildContext context) {
    final d = destination;
    return DraggableScrollableSheet(
      initialChildSize: 0.85,
      minChildSize: 0.5,
      maxChildSize: 0.95,
      expand: false,
      builder: (context, controller) => SingleChildScrollView(
        controller: controller,
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text(
                  'Destination Details',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Container(
              height: 180,
              width: double.infinity,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                gradient: const LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [AppColors.primary, AppColors.primaryDark],
                ),
              ),
              child: const Icon(Icons.landscape, color: Colors.white, size: 64),
            ),
            const SizedBox(height: 16),
            Text(
              d.name,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            Text(
              '${d.name} is a ${d.difficulty.toLowerCase()} trek in the '
              '${d.region} region of Nepal.',
              style: const TextStyle(
                color: AppColors.textSecondary,
                height: 1.4,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _FactBox(label: 'Duration', value: d.durationLabel),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _FactBox(label: 'Difficulty', value: d.difficulty),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _FactBox(
                    label: 'Max Altitude',
                    value: '${d.maxAltitudeM} m',
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _FactBox(
                    label: 'Best Season',
                    value: d.bestSeasonLabel,
                  ),
                ),
              ],
            ),
            if (d.permits.isNotEmpty) ...[
              const SizedBox(height: 20),
              const Text(
                'Permits required',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              ...d.permits.map(
                (p) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('•  '),
                      Expanded(child: Text(p)),
                    ],
                  ),
                ),
              ),
            ],
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  onFindGuide?.call();
                },
                child: const Text('Find a guide'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FactBox extends StatelessWidget {
  const _FactBox({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.primary.withValues(alpha: 0.06),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(
              color: AppColors.textSecondary,
              fontSize: 12.5,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }
}
