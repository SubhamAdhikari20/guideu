/// Pure domain entity for a trekking destination (a route in the catalog).
/// No Flutter or JSON here — mapped from the core-engine `TrekkingRoute`.
class Destination {
  const Destination({
    required this.id,
    required this.externalId,
    required this.name,
    required this.region,
    required this.difficulty,
    required this.difficultyLevel,
    required this.maxAltitudeM,
    required this.durationDays,
    required this.bestSeasons,
    required this.permits,
    required this.estimatedCostUsd,
    required this.badgePoints,
  });

  final int id;
  final String externalId;
  final String name;
  final String region;
  final String difficulty; // Easy | Moderate | Hard | Very Hard
  final int difficultyLevel; // 1..4
  final int maxAltitudeM;
  final int durationDays;
  final List<String> bestSeasons;
  final List<String> permits;
  final int estimatedCostUsd;
  final int badgePoints;

  /// Short human label for the duration, e.g. "14 days".
  String get durationLabel =>
      durationDays == 1 ? '1 day' : '$durationDays days';

  /// Best season range as a single string, e.g. "Oct-Dec, Mar-May".
  String get bestSeasonLabel =>
      bestSeasons.isEmpty ? 'All year' : bestSeasons.join(', ');
}
