import '../../domain/entities/auth_user.dart';

/// Data-layer model that maps the core-engine user JSON to the domain entity.
class AuthUserModel {
  const AuthUserModel({
    required this.id,
    required this.email,
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.role,
    this.phoneNumber,
    this.isGuideVerified = false,
  });

  final String id;
  final String email;
  final String username;
  final String firstName;
  final String lastName;
  final String role;
  final String? phoneNumber;
  final bool isGuideVerified;

  factory AuthUserModel.fromJson(Map<String, dynamic> json) => AuthUserModel(
        id: json['id'].toString(),
        email: (json['email'] ?? '') as String,
        username: (json['username'] ?? '') as String,
        firstName: (json['first_name'] ?? '') as String,
        lastName: (json['last_name'] ?? '') as String,
        role: (json['role'] ?? 'TOURIST') as String,
        phoneNumber: json['phone_number'] as String?,
        isGuideVerified: (json['is_guide_verified'] ?? false) as bool,
      );

  AuthUser toEntity() {
    final name = '$firstName $lastName'.trim();
    return AuthUser(
      id: id,
      email: email,
      fullName: name.isEmpty ? username : name,
      role: role,
      phoneNumber: phoneNumber,
      isGuideVerified: isGuideVerified,
    );
  }
}
