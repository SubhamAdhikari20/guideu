import '../../domain/entities/review.dart';

/// Maps the core-engine `Review` JSON to a [Review] entity.
class ReviewModel {
  const ReviewModel({
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
  final String status;
  final String createdAt;

  factory ReviewModel.fromJson(Map<String, dynamic> json) {
    return ReviewModel(
      id: json['id'] as int,
      authorUsername: (json['author_username'] ?? 'Traveller') as String,
      rating: (json['rating'] ?? 0) as int,
      title: (json['title'] ?? '') as String,
      comment: (json['comment'] ?? '') as String,
      status: (json['status'] ?? 'PENDING') as String,
      createdAt: (json['created_at'] ?? '') as String,
    );
  }

  Review toEntity() => Review(
        id: id,
        authorUsername: authorUsername,
        rating: rating,
        title: title,
        comment: comment,
        status: status,
        createdAt: DateTime.tryParse(createdAt) ?? DateTime.now(),
      );
}
