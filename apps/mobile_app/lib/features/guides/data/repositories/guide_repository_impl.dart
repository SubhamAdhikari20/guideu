import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/guide.dart';
import '../../domain/repositories/guide_repository.dart';
import '../datasources/guide_remote_datasource.dart';

class GuideRepositoryImpl implements GuideRepository {
  const GuideRepositoryImpl(this._remote);

  final GuideRemoteDataSource _remote;

  @override
  Future<(Failure?, List<Guide>?)> getGuides({String? search}) async {
    try {
      final models = await _remote.getGuides(search: search);
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
    var message = 'Could not load guides. Please try again.';
    if (data is Map && data['detail'] is String) {
      message = data['detail'] as String;
    }
    return ServerFailure(message, statusCode: code);
  }
}
