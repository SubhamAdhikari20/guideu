import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/review.dart';
import '../repositories/review_repository.dart';

/// Lists reviews for a guide.
class GetGuideReviewsUseCase implements UseCase<List<Review>, int> {
  const GetGuideReviewsUseCase(this._repository);

  final ReviewRepository _repository;

  @override
  Future<(Failure?, List<Review>?)> call(int guideId) {
    return _repository.getGuideReviews(guideId);
  }
}
