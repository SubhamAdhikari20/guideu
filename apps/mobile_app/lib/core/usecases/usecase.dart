import '../error/failures.dart';

/// Contract every use case implements (clean architecture).
///
/// Returns a record of `(Failure?, T?)` — a lightweight, dependency-free
/// alternative to `Either`: exactly one side is non-null. Feature use cases are
/// added in later sprints.
abstract interface class UseCase<T, Params> {
  Future<(Failure?, T?)> call(Params params);
}

/// Marker for use cases that take no parameters.
class NoParams {
  const NoParams();
}
