import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/review.dart';
import '../repositories/review_repository.dart';

class SubmitReviewParams {
  const SubmitReviewParams({
    required this.guideId,
    required this.rating,
    required this.title,
    required this.comment,
  });

  final int guideId;
  final int rating;
  final String title;
  final String comment;
}

/// Submits a review for a guide.
class SubmitReviewUseCase implements UseCase<Review, SubmitReviewParams> {
  const SubmitReviewUseCase(this._repository);

  final ReviewRepository _repository;

  @override
  Future<(Failure?, Review?)> call(SubmitReviewParams params) {
    return _repository.submitGuideReview(
      guideId: params.guideId,
      rating: params.rating,
      title: params.title,
      comment: params.comment,
    );
  }
}
