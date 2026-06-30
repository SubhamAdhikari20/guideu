import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/usecases/usecase.dart';
import '../../../auth/presentation/providers/auth_providers.dart';
import '../../data/datasources/booking_remote_datasource.dart';
import '../../data/repositories/booking_repository_impl.dart';
import '../../domain/entities/booking.dart';
import '../../domain/entities/tour_package.dart';
import '../../domain/repositories/booking_repository.dart';
import '../../domain/usecases/cancel_booking_usecase.dart';
import '../../domain/usecases/create_booking_usecase.dart';
import '../../domain/usecases/get_my_bookings_usecase.dart';
import '../../domain/usecases/get_packages_usecase.dart';

// ---- Dependency injection (clean architecture wiring) ----------------------

final bookingRemoteDataSourceProvider = Provider<BookingRemoteDataSource>(
  (ref) => BookingRemoteDataSource(ref.watch(apiClientProvider).dio),
);

final bookingRepositoryProvider = Provider<BookingRepository>(
  (ref) => BookingRepositoryImpl(ref.watch(bookingRemoteDataSourceProvider)),
);

final getPackagesUseCaseProvider = Provider<GetPackagesUseCase>(
  (ref) => GetPackagesUseCase(ref.watch(bookingRepositoryProvider)),
);

final getMyBookingsUseCaseProvider = Provider<GetMyBookingsUseCase>(
  (ref) => GetMyBookingsUseCase(ref.watch(bookingRepositoryProvider)),
);

final createBookingUseCaseProvider = Provider<CreateBookingUseCase>(
  (ref) => CreateBookingUseCase(ref.watch(bookingRepositoryProvider)),
);

final cancelBookingUseCaseProvider = Provider<CancelBookingUseCase>(
  (ref) => CancelBookingUseCase(ref.watch(bookingRepositoryProvider)),
);

// ---- Screen state ----------------------------------------------------------

/// Tour packages keyed by the search term (empty = all).
final packagesProvider =
    FutureProvider.family<List<TourPackage>, String>((ref, search) async {
  final (failure, data) =
      await ref.watch(getPackagesUseCaseProvider).call(PackageQuery(search: search));
  if (failure != null) throw failure;
  return data ?? const [];
});

/// The logged-in user's bookings.
final myBookingsProvider = FutureProvider<List<Booking>>((ref) async {
  final (failure, data) =
      await ref.watch(getMyBookingsUseCaseProvider).call(const NoParams());
  if (failure != null) throw failure;
  return data ?? const [];
});
