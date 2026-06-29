/// Pure domain entity for an authenticated user (no Flutter / JSON here).
class AuthUser {
  const AuthUser({
    required this.id,
    required this.email,
    required this.fullName,
    required this.role,
    this.phoneNumber,
    this.isGuideVerified = false,
  });

  final String id;
  final String email;
  final String fullName;
  final String role; // TOURIST | GUIDE | ADMIN
  final String? phoneNumber;
  final bool isGuideVerified;

  bool get isGuide => role == 'GUIDE';
  bool get isTourist => role == 'TOURIST';
}
