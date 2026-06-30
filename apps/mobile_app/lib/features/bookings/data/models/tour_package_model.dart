import '../../domain/entities/tour_package.dart';

/// Maps the core-engine `TourPackage` JSON to a [TourPackage] entity.
class TourPackageModel {
  const TourPackageModel({
    required this.id,
    required this.title,
    required this.description,
    required this.basePrice,
    required this.durationDays,
    required this.capacity,
  });

  final int id;
  final String title;
  final String description;
  final double basePrice;
  final int durationDays;
  final int capacity;

  factory TourPackageModel.fromJson(Map<String, dynamic> json) {
    return TourPackageModel(
      id: json['id'] as int,
      title: (json['title'] ?? '') as String,
      description: (json['description'] ?? '') as String,
      basePrice: _toDouble(json['base_price']),
      durationDays: (json['duration_days'] ?? 1) as int,
      capacity: (json['capacity'] ?? 1) as int,
    );
  }

  static double _toDouble(dynamic value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }

  TourPackage toEntity() => TourPackage(
        id: id,
        title: title,
        description: description,
        basePrice: basePrice,
        durationDays: durationDays,
        capacity: capacity,
      );
}
