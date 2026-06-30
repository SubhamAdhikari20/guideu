import '../../../../core/error/failures.dart';
import '../entities/auth_user.dart';
import '../repositories/auth_repository.dart';

class LoginParams {
  const LoginParams({required this.email, required this.password});
  final String email;
  final String password;
}

class LoginUseCase {
  const LoginUseCase(this._repository);
  final AuthRepository _repository;

  Future<(Failure?, AuthUser?)> call(LoginParams params) =>
      _repository.login(email: params.email, password: params.password);
}
