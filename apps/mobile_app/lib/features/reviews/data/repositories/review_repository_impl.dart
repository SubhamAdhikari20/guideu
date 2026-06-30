import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/review.dart';
import '../../domain/repositories/review_repository.dart';
import '../datasources/review_remote_datasource.dart';

class ReviewRepositoryImpl implements ReviewRepository {
  const ReviewRepositoryImpl(this._remote);

  final ReviewRemoteDataSource _remote;

  @override
  Future<(Failure?, List<Review>?)> getGuideReviews(int guideId) async {
    try {
      final models = await _remote.getGuideReviews(guideId);
      return (null, models.map((m) => m.toEntity()).toList());
    } on DioException catch (e) {
      return (_mapError(e, 'Could not load reviews.'), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  @override
  Future<(Failure?, ReviewSummary?)> getGuideSummary(int guideId) async {
    try {
      final summary = await _remote.getGuideSummary(guideId);
      return (null, summary);
    } on DioException catch (e) {
      return (_mapError(e, 'Could not load the rating.'), null);
    } catch (e) {
      return (ServerFailure(e.toString()), null);
    }
  }

  @override
  Future<(Failure?, Review?)> submitGuideReview({
    required int guideId,
    required int rating,
    required String title,
    required String comment,
  }) async {
    try {
      final model = await _remote.submitGuideReview(
        guideId: guideId,
        rating: rating,
        title: title,
        comment: comment,
      );
      return (null, model.toEntity());
    } on DioException catch (e) {
      return (_mapError(e, 'Could not submit your review.'), null);
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
