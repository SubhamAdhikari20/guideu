import '../../domain/entities/payment.dart';

/// Maps the core-engine `PaymentTransaction` JSON to a [Payment] entity.
class PaymentModel {
  const PaymentModel({
    required this.id,
    required this.booking,
    required this.amount,
    required this.currency,
    required this.status,
    required this.gateway,
  });

  final int id;
  final int? booking;
  final double amount;
  final String currency;
  final String status;
  final String gateway;

  factory PaymentModel.fromJson(Map<String, dynamic> json) {
    return PaymentModel(
      id: json['id'] as int,
      booking: json['booking'] as int?,
      amount: _toDouble(json['amount']),
      currency: (json['currency'] ?? 'NPR') as String,
      status: (json['status'] ?? 'PENDING') as String,
      gateway: (json['gateway'] ?? 'OTHER') as String,
    );
  }

  static double _toDouble(dynamic value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }

  Payment toEntity() => Payment(
        id: id,
        bookingId: booking,
        amount: amount,
        currency: currency,
        status: status,
        gateway: gateway,
      );
}
