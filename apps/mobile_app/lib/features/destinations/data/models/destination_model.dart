import '../../domain/entities/destination.dart';

/// Data model that maps the core-engine `TrekkingRoute` JSON to a [Destination].
class DestinationModel {
  const DestinationModel({
    required this.id,
    required this.externalId,
    required this.routeName,
    required this.region,
    required this.difficulty,
    required this.difficultyLevel,
    required this.maxAltitudeM,
    required this.durationDays,
    required this.bestSeasonList,
    required this.permitList,
    required this.estimatedCostUsd,
    required this.badgePoints,
  });

  final int id;
  final String externalId;
  final String routeName;
  final String region;
  final String difficulty;
  final int difficultyLevel;
  final int maxAltitudeM;
  final int durationDays;
  final List<String> bestSeasonList;
  final List<String> permitList;
  final int estimatedCostUsd;
  final int badgePoints;

  factory DestinationModel.fromJson(Map<String, dynamic> json) {
    return DestinationModel(
      id: json['id'] as int,
      externalId: (json['external_id'] ?? '') as String,
      routeName: (json['route_name'] ?? '') as String,
      region: (json['region'] ?? '') as String,
      difficulty: (json['difficulty'] ?? '') as String,
      difficultyLevel: (json['difficulty_level'] ?? 1) as int,
      maxAltitudeM: (json['max_altitude_m'] ?? 0) as int,
      durationDays: (json['duration_days'] ?? 0) as int,
      bestSeasonList: _stringList(json['best_season_list']),
      permitList: _stringList(json['permit_list']),
      estimatedCostUsd: (json['estimated_cost_usd'] ?? 0) as int,
      badgePoints: (json['badge_points'] ?? 0) as int,
    );
  }

  static List<String> _stringList(dynamic value) {
    if (value is List) {
      return value.map((e) => e.toString()).toList();
    }
    return const [];
  }

  Destination toEntity() {
    return Destination(
      id: id,
      externalId: externalId,
      name: routeName,
      region: region,
      difficulty: difficulty,
      difficultyLevel: difficultyLevel,
      maxAltitudeM: maxAltitudeM,
      durationDays: durationDays,
      bestSeasons: bestSeasonList,
      permits: permitList,
      estimatedCostUsd: estimatedCostUsd,
      badgePoints: badgePoints,
    );
  }
}
