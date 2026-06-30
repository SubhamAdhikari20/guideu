import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/review.dart';
import '../repositories/review_repository.dart';

/// Gets the aggregate rating for a guide.
class GetGuideSummaryUseCase implements UseCase<ReviewSummary, int> {
  const GetGuideSummaryUseCase(this._repository);

  final ReviewRepository _repository;

  @override
  Future<(Failure?, ReviewSummary?)> call(int guideId) {
    return _repository.getGuideSummary(guideId);
  }
}
