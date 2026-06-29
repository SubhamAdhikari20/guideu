/// Base failure type returned across the app (clean-architecture error model,
/// adapted from the leelame reference). Use cases surface a [Failure] instead of
/// throwing, so the presentation layer can render predictable error states.
sealed class Failure {
  const Failure(this.message);

  final String message;

  @override
  String toString() => '$runtimeType($message)';
}

class ServerFailure extends Failure {
  const ServerFailure(super.message, {this.statusCode});

  final int? statusCode;
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No internet connection']);
}

class CacheFailure extends Failure {
  const CacheFailure([super.message = 'Local cache error']);
}

class ValidationFailure extends Failure {
  const ValidationFailure(super.message);
}
