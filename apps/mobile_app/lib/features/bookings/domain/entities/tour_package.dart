/// Pure domain entity for a bookable tour package (core-engine `TourPackage`).
class TourPackage {
  const TourPackage({
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

  String get priceLabel => 'Rs. ${basePrice.toStringAsFixed(0)}';

  String get durationLabel =>
      durationDays == 1 ? '1 day' : '$durationDays days';
}
