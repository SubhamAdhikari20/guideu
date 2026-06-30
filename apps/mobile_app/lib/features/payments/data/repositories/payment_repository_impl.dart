import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/payment.dart';
import '../../domain/repositories/payment_repository.dart';
import '../datasources/payment_remote_datasource.dart';

class PaymentRepositoryImpl implements PaymentRepository {
  const PaymentRepositoryImpl(this._remote);

  final PaymentRemoteDataSource _remote;

  @override
  Future<(Failure?, Payment?)> initiate({
    required int bookingId,
    required double amount,
    required PaymentGateway gateway,
  }) async {
    try {
      final model = await _remote.initiate(
        bookingId: bookingId,
        amount: amount,
        gateway: gateway,
      );
      return (null, model.toEntity());
    } on DioException catch (e) {
      return (_mapError(e), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  @override
  Future<(Failure?, Payment?)> confirm(int paymentId) async {
    try {
      final model = await _remote.confirm(paymentId);
      return (null, model.toEntity());
    } on DioException catch (e) {
      return (_mapError(e), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  Failure _mapError(DioException e) {
    if (e.type == DioExceptionType.connectionError ||
        e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.receiveTimeout) {
      return const NetworkFailure();
    }
    final code = e.response?.statusCode;
    final data = e.response?.data;
    var message = 'Payment could not be completed. Please try again.';
    if (data is Map) {
      if (data['detail'] is String) {
        message = data['detail'] as String;
      } else if (data.isNotEmpty) {
        final firstVal = data.values.first;
        message = firstVal is List && firstVal.isNotEmpty
            ? firstVal.first.toString()
            : firstVal.toString();
      }
    }
    return ServerFailure(message, statusCode: code);
  }
}
