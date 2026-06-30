import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/tour_package.dart';
import '../repositories/booking_repository.dart';

class PackageQuery {
  const PackageQuery({this.search});

  final String? search;
}

/// Lists bookable tour packages.
class GetPackagesUseCase implements UseCase<List<TourPackage>, PackageQuery> {
  const GetPackagesUseCase(this._repository);

  final BookingRepository _repository;

  @override
  Future<(Failure?, List<TourPackage>?)> call(PackageQuery params) {
    return _repository.getPackages(search: params.search);
  }
}
