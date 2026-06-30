import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/booking.dart';
import '../../domain/entities/tour_package.dart';
import '../../domain/repositories/booking_repository.dart';
import '../datasources/booking_remote_datasource.dart';

class BookingRepositoryImpl implements BookingRepository {
  const BookingRepositoryImpl(this._remote);

  final BookingRemoteDataSource _remote;

  @override
  Future<(Failure?, List<TourPackage>?)> getPackages({String? search}) async {
    try {
      final models = await _remote.getPackages(search: search);
      return (null, models.map((m) => m.toEntity()).toList());
    } on DioException catch (e) {
      return (_mapError(e, 'Could not load tour packages.'), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  @override
  Future<(Failure?, Booking?)> createBooking({
    required int packageId,
    required DateTime startDate,
    required DateTime endDate,
    String notes = '',
  }) async {
    try {
      final model = await _remote.createBooking(
        packageId: packageId,
        startDate: startDate,
        endDate: endDate,
        notes: notes,
      );
      return (null, model.toEntity());
    } on DioException catch (e) {
      return (_mapError(e, 'Could not create the booking.'), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  @override
  Future<(Failure?, List<Booking>?)> getMyBookings() async {
    try {
      final models = await _remote.getMyBookings();
      return (null, models.map((m) => m.toEntity()).toList());
    } on DioException catch (e) {
      return (_mapError(e, 'Could not load your bookings.'), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  @override
  Future<(Failure?, Booking?)> cancelBooking(int bookingId) async {
    try {
      final model = await _remote.cancelBooking(bookingId);
      return (null, model.toEntity());
    } on DioException catch (e) {
      return (_mapError(e, 'Could not cancel the booking.'), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  Failure _mapError(DioException e, String fallback) {
    if (e.type == DioExceptionType.connectionError ||
        e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.receiveTimeout) {
      return const NetworkFailure();
    }
    final code = e.response?.statusCode;
    final data = e.response?.data;
    var message = fallback;
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
