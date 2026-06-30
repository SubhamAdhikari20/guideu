import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../constants/app_constants.dart';

/// Securely persists the JWT access/refresh pair (flutter_secure_storage).
class TokenStorage {
  TokenStorage([FlutterSecureStorage? storage])
      : _storage = storage ?? const FlutterSecureStorage();

  final FlutterSecureStorage _storage;

  Future<void> saveTokens({required String access, required String refresh}) async {
    await _storage.write(key: AppConstants.secureAccessTokenKey, value: access);
    await _storage.write(key: AppConstants.secureRefreshTokenKey, value: refresh);
  }

  Future<String?> getAccessToken() =>
      _storage.read(key: AppConstants.secureAccessTokenKey);

  Future<String?> getRefreshToken() =>
      _storage.read(key: AppConstants.secureRefreshTokenKey);

  Future<void> clear() async {
    await _storage.delete(key: AppConstants.secureAccessTokenKey);
    await _storage.delete(key: AppConstants.secureRefreshTokenKey);
  }
}
