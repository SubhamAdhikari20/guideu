import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../auth/presentation/providers/auth_providers.dart';
import '../../data/datasources/payment_remote_datasource.dart';
import '../../data/repositories/payment_repository_impl.dart';
import '../../domain/repositories/payment_repository.dart';
import '../../domain/usecases/pay_for_booking_usecase.dart';

// ---- Dependency injection (clean architecture wiring) ----------------------

final paymentRemoteDataSourceProvider = Provider<PaymentRemoteDataSource>(
  (ref) => PaymentRemoteDataSource(ref.watch(apiClientProvider).dio),
);

final paymentRepositoryProvider = Provider<PaymentRepository>(
  (ref) => PaymentRepositoryImpl(ref.watch(paymentRemoteDataSourceProvider)),
);

final payForBookingUseCaseProvider = Provider<PayForBookingUseCase>(
  (ref) => PayForBookingUseCase(ref.watch(paymentRepositoryProvider)),
);
