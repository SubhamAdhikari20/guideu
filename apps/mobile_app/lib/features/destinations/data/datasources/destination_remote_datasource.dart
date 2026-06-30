import 'package:dio/dio.dart';

import '../../../../core/api/api_endpoints.dart';
import '../models/destination_model.dart';

/// Reads trekking destinations from the core-engine catalog endpoints.
class DestinationRemoteDataSource {
  const DestinationRemoteDataSource(this._dio);

  final Dio _dio;

  Future<List<DestinationModel>> getDestinations({String? search}) async {
    final resp = await _dio.get(
      ApiEndpoints.routes,
      queryParameters: <String, dynamic>{
        if (search != null && search.isNotEmpty) 'search': search,
        'ordering': '-badge_points',
      },
    );
    final results = _resultsOf(resp.data);
    return results
        .map((e) => DestinationModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// The catalog uses page-number pagination (`{count, next, previous, results}`),
  /// but tolerate a bare list too.
  List<dynamic> _resultsOf(dynamic data) {
    if (data is Map && data['results'] is List) {
      return data['results'] as List<dynamic>;
    }
    if (data is List) return data;
    return const [];
  }
}
