import '../../../../core/error/failures.dart';
import '../entities/review.dart';

/// Contract for reading and writing reviews (clean architecture).
abstract interface class ReviewRepository {
  Future<(Failure?, List<Review>?)> getGuideReviews(int guideId);

  Future<(Failure?, ReviewSummary?)> getGuideSummary(int guideId);

  Future<(Failure?, Review?)> submitGuideReview({
    required int guideId,
    required int rating,
    required String title,
    required String comment,
  });
}
