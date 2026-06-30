import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/booking.dart';
import '../repositories/booking_repository.dart';

/// Lists the logged-in user's bookings.
class GetMyBookingsUseCase implements UseCase<List<Booking>, NoParams> {
  const GetMyBookingsUseCase(this._repository);

  final BookingRepository _repository;

  @override
  Future<(Failure?, List<Booking>?)> call(NoParams params) {
    return _repository.getMyBookings();
  }
}
