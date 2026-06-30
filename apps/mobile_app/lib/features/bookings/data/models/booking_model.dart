import '../../domain/entities/booking.dart';

/// Maps the core-engine `BookingSession` JSON to a [Booking] entity.
class BookingModel {
  const BookingModel({
    required this.id,
    required this.bookingReference,
    required this.tourPackage,
    required this.tourPackageTitle,
    required this.startDate,
    required this.endDate,
    required this.status,
    required this.totalPrice,
    required this.notes,
  });

  final int id;
  final String bookingReference;
  final int tourPackage;
  final String tourPackageTitle;
  final String startDate;
  final String endDate;
  final String status;
  final double totalPrice;
  final String notes;

  factory BookingModel.fromJson(Map<String, dynamic> json) {
    return BookingModel(
      id: json['id'] as int,
      bookingReference: (json['booking_reference'] ?? '') as String,
      tourPackage: (json['tour_package'] ?? 0) as int,
      tourPackageTitle: (json['tour_package_title'] ?? 'Tour package') as String,
      startDate: (json['start_date'] ?? '') as String,
      endDate: (json['end_date'] ?? '') as String,
      status: (json['status'] ?? 'PENDING') as String,
      totalPrice: _toDouble(json['total_price']),
      notes: (json['notes'] ?? '') as String,
    );
  }

  static double _toDouble(dynamic value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }

  Booking toEntity() => Booking(
        id: id,
        bookingReference: bookingReference,
        tourPackageId: tourPackage,
        tourPackageTitle: tourPackageTitle,
        startDate: DateTime.tryParse(startDate) ?? DateTime.now(),
        endDate: DateTime.tryParse(endDate) ?? DateTime.now(),
        status: BookingStatus.fromApi(status),
        totalPrice: totalPrice,
        notes: notes,
      );
}
