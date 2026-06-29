import 'package:dio/dio.dart';

import 'api_endpoints.dart';

/// Thin wrapper around [Dio] with GuideU defaults and a hook for attaching a
/// bearer token. Feature remote datasources depend on this (clean architecture);
/// the concrete token provider is wired in with the auth feature in sprint-2.
class ApiClient {
  ApiClient({Dio? dio, this.tokenProvider}) : _dio = dio ?? Dio() {
    _dio.options
      ..baseUrl = ApiEndpoints.baseUrl
      ..connectTimeout = ApiEndpoints.connectTimeout
      ..receiveTimeout = ApiEndpoints.receiveTimeout
      ..headers = <String, dynamic>{'Content-Type': 'application/json'};

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          final token = tokenProvider?.call();
          if (token != null && token.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          handler.next(options);
        },
      ),
    );
  }

  /// Supplies the current access token (or null when unauthenticated).
  final String? Function()? tokenProvider;

  final Dio _dio;

  Dio get dio => _dio;
}
