/// Central registry of backend endpoints.
///
/// The base URL is compile-time configurable via `--dart-define`; the default
/// targets the Android emulator's host alias for a locally running core-engine.
class ApiEndpoints {
  ApiEndpoints._();

  static const String baseUrl = String.fromEnvironment(
    'GUIDEU_API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api/v1',
  );

  static const Duration connectTimeout = Duration(seconds: 20);
  static const Duration receiveTimeout = Duration(seconds: 20);

  // Auth (core-engine)
  static const String login = '/auth/token/';
  static const String refresh = '/auth/token/refresh/';
  static const String register = '/auth/register/';
  static const String me = '/auth/users/me/';
}
