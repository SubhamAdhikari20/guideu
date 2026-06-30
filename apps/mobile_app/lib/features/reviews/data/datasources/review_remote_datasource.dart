import 'package:dio/dio.dart';

import '../../../../core/api/api_endpoints.dart';
import '../../domain/entities/review.dart';
import '../models/review_model.dart';

/// Talks to the core-engine reviews endpoints over Dio.
class ReviewRemoteDataSource {
  const ReviewRemoteDataSource(this._dio);

  final Dio _dio;

  Future<List<ReviewModel>> getGuideReviews(int guideId) async {
    final resp = await _dio.get(
      ApiEndpoints.reviews,
      queryParameters: <String, dynamic>{'guide': guideId, 'ordering': '-created_at'},
    );
    return _resultsOf(resp.data)
        .map((e) => ReviewModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<ReviewSummary> getGuideSummary(int guideId) async {
    final resp = await _dio.get(
      ApiEndpoints.reviewSummary,
      queryParameters: <String, dynamic>{'guide': guideId},
    );
    final data = resp.data as Map<String, dynamic>;
    return ReviewSummary(
      averageRating: _toDouble(data['average_rating']),
      reviewCount: (data['review_count'] ?? 0) as int,
    );
  }

  Future<ReviewModel> submitGuideReview({
    required int guideId,
    required int rating,
    required String title,
    required String comment,
  }) async {
    final resp = await _dio.post(
      ApiEndpoints.reviews,
      data: <String, dynamic>{
        'guide': guideId,
        'rating': rating,
        if (title.isNotEmpty) 'title': title,
        if (comment.isNotEmpty) 'comment': comment,
      },
    );
    return ReviewModel.fromJson(resp.data as Map<String, dynamic>);
  }

  static double _toDouble(dynamic value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }

  List<dynamic> _resultsOf(dynamic data) {
    if (data is Map && data['results'] is List) {
      return data['results'] as List<dynamic>;
    }
    if (data is List) return data;
    return const [];
  }
}
