/// JWT pair returned by the core-engine token endpoint.
class AuthTokenModel {
  const AuthTokenModel({required this.access, required this.refresh});

  final String access;
  final String refresh;

  factory AuthTokenModel.fromJson(Map<String, dynamic> json) => AuthTokenModel(
        access: json['access'] as String,
        refresh: json['refresh'] as String,
      );
}
