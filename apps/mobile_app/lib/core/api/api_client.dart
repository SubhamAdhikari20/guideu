import 'package:dio/dio.dart';

import '../storage/token_storage.dart';
import 'api_endpoints.dart';

/// Configured [Dio] for GuideU. Attaches the bearer token to every request and
/// transparently refreshes it once on a 401 (clean-architecture data layer
/// depends on this). The concrete token store is injected.
class ApiClient {
  ApiClient({Dio? dio, required this.tokenStorage}) : _dio = dio ?? Dio() {
    _dio.options
      ..baseUrl = ApiEndpoints.baseUrl
      ..connectTimeout = ApiEndpoints.connectTimeout
      ..receiveTimeout = ApiEndpoints.receiveTimeout
      ..headers = <String, dynamic>{'Content-Type': 'application/json'};

    _dio.interceptors.add(_AuthInterceptor(_dio, tokenStorage));
  }

  final Dio _dio;
  final TokenStorage tokenStorage;

  Dio get dio => _dio;
}

class _AuthInterceptor extends QueuedInterceptor {
  _AuthInterceptor(this._dio, this._tokenStorage);

  final Dio _dio;
  final TokenStorage _tokenStorage;

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await _tokenStorage.getAccessToken();
    if (token != null && token.isNotEmpty) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final isAuthCall = err.requestOptions.path.contains('/auth/token');
    if (err.response?.statusCode == 401 && !isAuthCall) {
      final refresh = await _tokenStorage.getRefreshToken();
      if (refresh != null && refresh.isNotEmpty) {
        try {
          final resp = await _dio.post(
            ApiEndpoints.refresh,
            data: <String, dynamic>{'refresh': refresh},
            options: Options(headers: <String, dynamic>{'Authorization': null}),
          );
          final newAccess = (resp.data as Map)['access'] as String?;
          if (newAccess != null) {
            await _tokenStorage.saveTokens(access: newAccess, refresh: refresh);
            final retry = err.requestOptions;
            retry.headers['Authorization'] = 'Bearer $newAccess';
            final clone = await _dio.fetch<dynamic>(retry);
            return handler.resolve(clone);
          }
        } on DioException catch (_) {
          await _tokenStorage.clear();
        }
      }
    }
    handler.next(err);
  }
}
