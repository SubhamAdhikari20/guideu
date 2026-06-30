import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/guide.dart';
import '../repositories/guide_repository.dart';

/// Parameters for [GetGuidesUseCase].
class GuideQuery {
  const GuideQuery({this.search});

  final String? search;
}

/// Fetches the list of verified guides from the catalog registry.
class GetGuidesUseCase implements UseCase<List<Guide>, GuideQuery> {
  const GetGuidesUseCase(this._repository);

  final GuideRepository _repository;

  @override
  Future<(Failure?, List<Guide>?)> call(GuideQuery params) {
    return _repository.getGuides(search: params.search);
  }
}
