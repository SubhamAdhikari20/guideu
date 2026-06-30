import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../auth/presentation/providers/auth_providers.dart';
import '../../data/datasources/guide_remote_datasource.dart';
import '../../data/repositories/guide_repository_impl.dart';
import '../../domain/entities/guide.dart';
import '../../domain/repositories/guide_repository.dart';
import '../../domain/usecases/get_guides_usecase.dart';

// ---- Dependency injection (clean architecture wiring) ----------------------

final guideRemoteDataSourceProvider = Provider<GuideRemoteDataSource>(
  (ref) => GuideRemoteDataSource(ref.watch(apiClientProvider).dio),
);

final guideRepositoryProvider = Provider<GuideRepository>(
  (ref) => GuideRepositoryImpl(ref.watch(guideRemoteDataSourceProvider)),
);

final getGuidesUseCaseProvider = Provider<GetGuidesUseCase>(
  (ref) => GetGuidesUseCase(ref.watch(guideRepositoryProvider)),
);

// ---- Screen state ----------------------------------------------------------

/// Verified guides keyed by the search term (empty string = all). Exposed as an
/// [AsyncValue] so the UI gets loading / error / data states for free.
final guidesProvider =
    FutureProvider.family<List<Guide>, String>((ref, search) async {
  final (failure, data) =
      await ref.watch(getGuidesUseCaseProvider).call(GuideQuery(search: search));
  if (failure != null) throw failure;
  return data ?? const [];
});
