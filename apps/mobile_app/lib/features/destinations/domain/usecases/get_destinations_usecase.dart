import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/destination.dart';
import '../repositories/destination_repository.dart';

/// Parameters for [GetDestinationsUseCase].
class DestinationQuery {
  const DestinationQuery({this.search});

  final String? search;
}

/// Fetches the list of trekking destinations from the catalog.
class GetDestinationsUseCase
    implements UseCase<List<Destination>, DestinationQuery> {
  const GetDestinationsUseCase(this._repository);

  final DestinationRepository _repository;

  @override
  Future<(Failure?, List<Destination>?)> call(DestinationQuery params) {
    return _repository.getDestinations(search: params.search);
  }
}
