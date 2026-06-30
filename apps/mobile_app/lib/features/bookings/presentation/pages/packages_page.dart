import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme/app_colors.dart';
import '../../../../core/error/failures.dart';
import '../providers/booking_providers.dart';
import '../widgets/book_package_sheet.dart';
import '../widgets/package_card.dart';
import 'my_bookings_page.dart';

/// Browse bookable tour packages.
class PackagesPage extends ConsumerWidget {
  const PackagesPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final packages = ref.watch(packagesProvider(''));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Tour Packages'),
        actions: [
          IconButton(
            tooltip: 'My bookings',
            icon: const Icon(Icons.receipt_long_outlined),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => const MyBookingsPage()),
            ),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => ref.refresh(packagesProvider('').future),
        child: packages.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => _ErrorState(
            message: error is Failure ? error.message : 'Something went wrong.',
            onRetry: () => ref.invalidate(packagesProvider('')),
          ),
          data: (items) {
            if (items.isEmpty) {
              return ListView(
                children: const [
                  SizedBox(height: 120),
                  Center(
                    child: Text(
                      'No tour packages yet.',
                      style: TextStyle(color: AppColors.textSecondary),
                    ),
                  ),
                ],
              );
            }
            return ListView(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
              children: [
                for (final p in items)
                  PackageCard(
                    package: p,
                    onTap: () async {
                      final booked = await showBookPackageSheet(context, p);
                      if (booked == true && context.mounted) {
                        _showBookedSnack(context);
                      }
                    },
                  ),
              ],
            );
          },
        ),
      ),
    );
  }

  void _showBookedSnack(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Booking created. Pay to confirm it.'),
        action: SnackBarAction(
          label: 'My bookings',
          onPressed: () => Navigator.of(context).push(
            MaterialPageRoute(builder: (_) => const MyBookingsPage()),
          ),
        ),
      ),
    );
  }
}

class _ErrorState extends StatelessWidget {
  const _ErrorState({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        const SizedBox(height: 100),
        Center(
          child: Column(
            children: [
              const Icon(Icons.cloud_off, size: 40, color: AppColors.textSecondary),
              const SizedBox(height: 12),
              Text(message, textAlign: TextAlign.center),
              const SizedBox(height: 12),
              OutlinedButton(onPressed: onRetry, child: const Text('Retry')),
            ],
          ),
        ),
      ],
    );
  }
}
