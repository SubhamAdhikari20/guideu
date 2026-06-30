import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/booking.dart';
import '../repositories/booking_repository.dart';

/// Cancels one of the user's bookings.
class CancelBookingUseCase implements UseCase<Booking, int> {
  const CancelBookingUseCase(this._repository);

  final BookingRepository _repository;

  @override
  Future<(Failure?, Booking?)> call(int bookingId) {
    return _repository.cancelBooking(bookingId);
  }
}
