import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../auth/presentation/providers/auth_providers.dart';
import '../../data/datasources/destination_remote_datasource.dart';
import '../../data/repositories/destination_repository_impl.dart';
import '../../domain/entities/destination.dart';
import '../../domain/repositories/destination_repository.dart';
import '../../domain/usecases/get_destinations_usecase.dart';

// ---- Dependency injection (clean architecture wiring) ----------------------

final destinationRemoteDataSourceProvider =
    Provider<DestinationRemoteDataSource>(
  (ref) => DestinationRemoteDataSource(ref.watch(apiClientProvider).dio),
);

final destinationRepositoryProvider = Provider<DestinationRepository>(
  (ref) => DestinationRepositoryImpl(
    ref.watch(destinationRemoteDataSourceProvider),
  ),
);

final getDestinationsUseCaseProvider = Provider<GetDestinationsUseCase>(
  (ref) => GetDestinationsUseCase(ref.watch(destinationRepositoryProvider)),
);

// ---- Screen state ----------------------------------------------------------

/// Destinations list keyed by the search term (empty string = all). Exposed as
/// an [AsyncValue] so the UI gets loading / error / data states for free; the
/// page passes its current query and the family re-fetches when it changes.
final destinationsProvider =
    FutureProvider.family<List<Destination>, String>((ref, search) async {
  final (failure, data) = await ref
      .watch(getDestinationsUseCaseProvider)
      .call(DestinationQuery(search: search));
  if (failure != null) throw failure;
  return data ?? const [];
});
