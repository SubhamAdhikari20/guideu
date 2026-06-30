import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/booking.dart';
import '../repositories/booking_repository.dart';

class CreateBookingParams {
  const CreateBookingParams({
    required this.packageId,
    required this.startDate,
    required this.endDate,
    this.notes = '',
  });

  final int packageId;
  final DateTime startDate;
  final DateTime endDate;
  final String notes;
}

/// Creates a booking for a tour package.
class CreateBookingUseCase implements UseCase<Booking, CreateBookingParams> {
  const CreateBookingUseCase(this._repository);

  final BookingRepository _repository;

  @override
  Future<(Failure?, Booking?)> call(CreateBookingParams params) {
    return _repository.createBooking(
      packageId: params.packageId,
      startDate: params.startDate,
      endDate: params.endDate,
      notes: params.notes,
    );
  }
}
