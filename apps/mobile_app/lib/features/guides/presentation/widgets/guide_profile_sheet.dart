import 'package:flutter/material.dart';

import '../../../../app/theme/app_colors.dart';
import '../../domain/entities/guide.dart';

/// Opens the "Guide Profile" bottom sheet for a [Guide], matching the prototype:
/// avatar, name, rating, about, experience & certification, languages and the
/// regions they cover.
Future<void> showGuideProfileSheet(BuildContext context, Guide guide) {
  return showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    backgroundColor: AppColors.surface,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (context) => _GuideProfileSheet(guide: guide),
  );
}

class _GuideProfileSheet extends StatelessWidget {
  const _GuideProfileSheet({required this.guide});

  final Guide guide;

  @override
  Widget build(BuildContext context) {
    final g = guide;
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
                  'Guide Profile',
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
            Center(
              child: Column(
                children: [
                  Container(
                    width: 84,
                    height: 84,
                    decoration: const BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [AppColors.primary, AppColors.primaryDark],
                      ),
                    ),
                    child: const Icon(Icons.person, color: Colors.white, size: 44),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        g.guideCode,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (g.isVerified) ...[
                        const SizedBox(width: 6),
                        const Icon(Icons.verified,
                            size: 18, color: AppColors.primary),
                      ],
                    ],
                  ),
                  const SizedBox(height: 2),
                  Text(
                    g.certification,
                    style: const TextStyle(color: AppColors.textSecondary),
                  ),
                  const SizedBox(height: 6),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.star, size: 18, color: AppColors.gold),
                      const SizedBox(width: 4),
                      Text(
                        '${g.ratingLabel}  •  ${g.totalTripsCompleted} trips',
                        style: const TextStyle(fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            const _SectionTitle('About'),
            const SizedBox(height: 6),
            Text(
              'Licensed guide registered with the Nepal Tourism Board '
              '(${g.ntbLicenseNo}), with ${g.experienceLabel} guiding trips '
              'across Nepal.',
              style: const TextStyle(
                color: AppColors.textSecondary,
                height: 1.4,
              ),
            ),
            const SizedBox(height: 20),
            const _SectionTitle('Experience & Certifications'),
            const SizedBox(height: 8),
            _IconLine(icon: Icons.schedule, text: g.experienceLabel),
            const SizedBox(height: 6),
            _IconLine(icon: Icons.workspace_premium, text: g.certification),
            if (g.languages.isNotEmpty) ...[
              const SizedBox(height: 20),
              const _SectionTitle('Languages'),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [for (final l in g.languages) _Chip(l)],
              ),
            ],
            if (g.regions.isNotEmpty) ...[
              const SizedBox(height: 20),
              const _SectionTitle('Regions covered'),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [for (final r in g.regions) _Chip(r)],
              ),
            ],
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Guide booking arrives in the next update.'),
                    ),
                  );
                },
                child: const Text('Book this guide'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.text);

  final String text;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
    );
  }
}

class _IconLine extends StatelessWidget {
  const _IconLine({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 18, color: AppColors.textSecondary),
        const SizedBox(width: 10),
        Expanded(child: Text(text)),
      ],
    );
  }
}

class _Chip extends StatelessWidget {
  const _Chip(this.label);

  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
      decoration: BoxDecoration(
        color: AppColors.primary.withValues(alpha: 0.10),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Text(
        label,
        style: const TextStyle(
          color: AppColors.primaryDark,
          fontSize: 12.5,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }
}
