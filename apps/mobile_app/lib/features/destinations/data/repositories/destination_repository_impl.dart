import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/destination.dart';
import '../../domain/repositories/destination_repository.dart';
import '../datasources/destination_remote_datasource.dart';

class DestinationRepositoryImpl implements DestinationRepository {
  const DestinationRepositoryImpl(this._remote);

  final DestinationRemoteDataSource _remote;

  @override
  Future<(Failure?, List<Destination>?)> getDestinations({String? search}) async {
    try {
      final models = await _remote.getDestinations(search: search);
      return (null, models.map((m) => m.toEntity()).toList());
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
    var message = 'Could not load destinations. Please try again.';
    if (data is Map && data['detail'] is String) {
      message = data['detail'] as String;
    }
    return ServerFailure(message, statusCode: code);
  }
}
