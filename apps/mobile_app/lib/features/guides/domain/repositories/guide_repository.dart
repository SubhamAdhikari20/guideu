import '../../../../core/error/failures.dart';
import '../entities/guide.dart';

/// Contract for reading verified guides (clean architecture — data layer
/// implements this).
abstract interface class GuideRepository {
  /// Lists active, verified guides, optionally filtered by a search term.
  Future<(Failure?, List<Guide>?)> getGuides({String? search});
}
