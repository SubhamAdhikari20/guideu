/// Pure domain entity for a review (core-engine `Review`).
class Review {
  const Review({
    required this.id,
    required this.authorUsername,
    required this.rating,
    required this.title,
    required this.comment,
    required this.status,
    required this.createdAt,
  });

  final int id;
  final String authorUsername;
  final int rating;
  final String title;
  final String comment;
  final String status; // PENDING | APPROVED | REJECTED
  final DateTime createdAt;

  bool get isApproved => status.toUpperCase() == 'APPROVED';
  bool get isPending => status.toUpperCase() == 'PENDING';
}

/// Aggregate rating for a guide or route.
class ReviewSummary {
  const ReviewSummary({required this.averageRating, required this.reviewCount});

  final double averageRating;
  final int reviewCount;

  String get ratingLabel => averageRating.toStringAsFixed(1);
}
