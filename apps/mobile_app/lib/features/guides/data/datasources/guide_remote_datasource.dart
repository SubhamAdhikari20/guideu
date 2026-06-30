import 'package:dio/dio.dart';

import '../../../../core/api/api_endpoints.dart';
import '../models/guide_model.dart';

/// Reads verified guides from the core-engine catalog registry endpoint.
class GuideRemoteDataSource {
  const GuideRemoteDataSource(this._dio);

  final Dio _dio;

  Future<List<GuideModel>> getGuides({String? search}) async {
    final resp = await _dio.get(
      ApiEndpoints.guidesRegistry,
      queryParameters: <String, dynamic>{
        if (search != null && search.isNotEmpty) 'search': search,
        'ordering': '-average_rating',
      },
    );
    final results = _resultsOf(resp.data);
    return results
        .map((e) => GuideModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  List<dynamic> _resultsOf(dynamic data) {
    if (data is Map && data['results'] is List) {
      return data['results'] as List<dynamic>;
    }
    if (data is List) return data;
    return const [];
  }
}
