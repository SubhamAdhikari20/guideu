import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/payment.dart';
import '../repositories/payment_repository.dart';

class PayForBookingParams {
  const PayForBookingParams({
    required this.bookingId,
    required this.amount,
    required this.gateway,
  });

  final int bookingId;
  final double amount;
  final PaymentGateway gateway;
}

/// Pays for a booking: creates the payment, then confirms it. Confirmation is a
/// stand-in for the real gateway callback (sandbox integration comes later).
class PayForBookingUseCase implements UseCase<Payment, PayForBookingParams> {
  const PayForBookingUseCase(this._repository);

  final PaymentRepository _repository;

  @override
  Future<(Failure?, Payment?)> call(PayForBookingParams params) async {
    final (initFailure, payment) = await _repository.initiate(
      bookingId: params.bookingId,
      amount: params.amount,
      gateway: params.gateway,
    );
    if (initFailure != null || payment == null) {
      return (initFailure, null);
    }
    return _repository.confirm(payment.id);
  }
}
