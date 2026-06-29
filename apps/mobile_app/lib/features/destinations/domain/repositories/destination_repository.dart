import '../../../../core/error/failures.dart';
import '../entities/destination.dart';

/// Contract for reading trekking destinations (clean architecture — the data
/// layer implements this, the domain only depends on the interface).
abstract interface class DestinationRepository {
  /// Lists published destinations, optionally filtered by a search term.
  Future<(Failure?, List<Destination>?)> getDestinations({String? search});
}
