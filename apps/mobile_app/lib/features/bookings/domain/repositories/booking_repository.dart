import '../../../../core/error/failures.dart';
import '../entities/booking.dart';
import '../entities/tour_package.dart';

/// Contract for tour packages and bookings (clean architecture).
abstract interface class BookingRepository {
  Future<(Failure?, List<TourPackage>?)> getPackages({String? search});

  Future<(Failure?, Booking?)> createBooking({
    required int packageId,
    required DateTime startDate,
    required DateTime endDate,
    String notes,
  });

  Future<(Failure?, List<Booking>?)> getMyBookings();

  Future<(Failure?, Booking?)> cancelBooking(int bookingId);
}
