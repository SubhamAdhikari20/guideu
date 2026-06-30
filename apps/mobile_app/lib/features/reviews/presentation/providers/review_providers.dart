import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../auth/presentation/providers/auth_providers.dart';
import '../../data/datasources/review_remote_datasource.dart';
import '../../data/repositories/review_repository_impl.dart';
import '../../domain/entities/review.dart';
import '../../domain/repositories/review_repository.dart';
import '../../domain/usecases/get_guide_reviews_usecase.dart';
import '../../domain/usecases/get_guide_summary_usecase.dart';
import '../../domain/usecases/submit_review_usecase.dart';

// ---- Dependency injection (clean architecture wiring) ----------------------

final reviewRemoteDataSourceProvider = Provider<ReviewRemoteDataSource>(
  (ref) => ReviewRemoteDataSource(ref.watch(apiClientProvider).dio),
);

final reviewRepositoryProvider = Provider<ReviewRepository>(
  (ref) => ReviewRepositoryImpl(ref.watch(reviewRemoteDataSourceProvider)),
);

final getGuideReviewsUseCaseProvider = Provider<GetGuideReviewsUseCase>(
  (ref) => GetGuideReviewsUseCase(ref.watch(reviewRepositoryProvider)),
);

final getGuideSummaryUseCaseProvider = Provider<GetGuideSummaryUseCase>(
  (ref) => GetGuideSummaryUseCase(ref.watch(reviewRepositoryProvider)),
);

final submitReviewUseCaseProvider = Provider<SubmitReviewUseCase>(
  (ref) => SubmitReviewUseCase(ref.watch(reviewRepositoryProvider)),
);

// ---- Screen state (keyed by guide id) --------------------------------------

final guideReviewsProvider =
    FutureProvider.family<List<Review>, int>((ref, guideId) async {
  final (failure, data) =
      await ref.watch(getGuideReviewsUseCaseProvider).call(guideId);
  if (failure != null) throw failure;
  return data ?? const [];
});

final guideReviewSummaryProvider =
    FutureProvider.family<ReviewSummary, int>((ref, guideId) async {
  final (failure, data) =
      await ref.watch(getGuideSummaryUseCaseProvider).call(guideId);
  if (failure != null) throw failure;
  return data ?? const ReviewSummary(averageRating: 0, reviewCount: 0);
});
