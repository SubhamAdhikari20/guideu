import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme/app_colors.dart';
import '../../domain/entities/review.dart';
import '../providers/review_providers.dart';

/// Shows a guide's rating summary and recent reviews. Used inside the guide
/// profile sheet. Keeps itself in sync via the review providers.
class GuideReviewsSection extends ConsumerWidget {
  const GuideReviewsSection({required this.guideId, super.key});

  final int guideId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summary = ref.watch(guideReviewSummaryProvider(guideId));
    final reviews = ref.watch(guideReviewsProvider(guideId));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Text(
              'Reviews',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const Spacer(),
            summary.maybeWhen(
              data: (s) => s.reviewCount == 0
                  ? const SizedBox.shrink()
                  : Row(
                      children: [
                        const Icon(Icons.star, size: 16, color: AppColors.gold),
                        const SizedBox(width: 3),
                        Text(
                          '${s.ratingLabel} (${s.reviewCount})',
                          style: const TextStyle(fontWeight: FontWeight.w600),
                        ),
                      ],
                    ),
              orElse: () => const SizedBox.shrink(),
            ),
          ],
        ),
        const SizedBox(height: 8),
        reviews.when(
          loading: () => const Padding(
            padding: EdgeInsets.symmetric(vertical: 12),
            child: Center(child: CircularProgressIndicator()),
          ),
          error: (_, _) => const Text(
            'Could not load reviews.',
            style: TextStyle(color: AppColors.textSecondary),
          ),
          data: (items) {
            if (items.isEmpty) {
              return const Text(
                'No reviews yet. Be the first to review this guide.',
                style: TextStyle(color: AppColors.textSecondary),
              );
            }
            return Column(
              children: [
                for (final r in items.take(5)) _ReviewTile(review: r),
              ],
            );
          },
        ),
      ],
    );
  }
}

class _ReviewTile extends StatelessWidget {
  const _ReviewTile({required this.review});

  final Review review;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.primary.withValues(alpha: 0.04),
        borderRadius: BorderRadius.circular(10),
        border: const Border(
          left: BorderSide(color: AppColors.primary, width: 3),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              for (var i = 1; i <= 5; i++)
                Icon(
                  i <= review.rating ? Icons.star : Icons.star_border,
                  size: 15,
                  color: AppColors.gold,
                ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  review.authorUsername,
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              if (review.isPending)
                const Text(
                  'pending',
                  style: TextStyle(color: AppColors.textSecondary, fontSize: 11),
                ),
            ],
          ),
          if (review.title.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(review.title, style: const TextStyle(fontWeight: FontWeight.w600)),
          ],
          if (review.comment.isNotEmpty) ...[
            const SizedBox(height: 2),
            Text(
              review.comment,
              style: const TextStyle(color: AppColors.textSecondary, fontSize: 13),
            ),
          ],
        ],
      ),
    );
  }
}
