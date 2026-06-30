/// Booking status mirroring the core-engine `BookingSession.Status`.
enum BookingStatus {
  pending,
  confirmed,
  active,
  completed,
  cancelled;

  static BookingStatus fromApi(String value) {
    switch (value.toUpperCase()) {
      case 'CONFIRMED':
        return BookingStatus.confirmed;
      case 'ACTIVE':
        return BookingStatus.active;
      case 'COMPLETED':
        return BookingStatus.completed;
      case 'CANCELLED':
        return BookingStatus.cancelled;
      case 'PENDING':
      default:
        return BookingStatus.pending;
    }
  }

  String get label {
    switch (this) {
      case BookingStatus.pending:
        return 'Pending payment';
      case BookingStatus.confirmed:
        return 'Confirmed';
      case BookingStatus.active:
        return 'Active';
      case BookingStatus.completed:
        return 'Completed';
      case BookingStatus.cancelled:
        return 'Cancelled';
    }
  }
}

/// Pure domain entity for a booking (core-engine `BookingSession`).
class Booking {
  const Booking({
    required this.id,
    required this.bookingReference,
    required this.tourPackageId,
    required this.tourPackageTitle,
    required this.startDate,
    required this.endDate,
    required this.status,
    required this.totalPrice,
    this.notes = '',
  });

  final int id;
  final String bookingReference;
  final int tourPackageId;
  final String tourPackageTitle;
  final DateTime startDate;
  final DateTime endDate;
  final BookingStatus status;
  final double totalPrice;
  final String notes;

  String get priceLabel => 'Rs. ${totalPrice.toStringAsFixed(0)}';

  bool get isPending => status == BookingStatus.pending;
  bool get isCompleted => status == BookingStatus.completed;
  bool get canCancel =>
      status == BookingStatus.pending || status == BookingStatus.confirmed;
}
