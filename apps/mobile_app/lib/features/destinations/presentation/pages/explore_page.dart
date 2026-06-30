import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme/app_colors.dart';
import '../../../../core/error/failures.dart';
import '../providers/destination_providers.dart';
import '../widgets/destination_card.dart';
import '../widgets/destination_detail_sheet.dart';

/// Explore tab — search and browse trekking destinations from the catalog.
/// [onFindGuide] lets the parent shell switch to the Guides tab.
class ExplorePage extends ConsumerStatefulWidget {
  const ExplorePage({this.onFindGuide, super.key});

  final VoidCallback? onFindGuide;

  @override
  ConsumerState<ExplorePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends ConsumerState<ExplorePage> {
  final _searchController = TextEditingController();
  String _query = '';

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _onSearch(String value) {
    setState(() => _query = value.trim());
  }

  @override
  Widget build(BuildContext context) {
    final destinations = ref.watch(destinationsProvider(_query));

    return Scaffold(
      appBar: AppBar(title: const Text('Explore')),
      body: RefreshIndicator(
        onRefresh: () => ref.refresh(destinationsProvider(_query).future),
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
          children: [
            _SearchField(
              controller: _searchController,
              onSubmitted: _onSearch,
            ),
            const SizedBox(height: 16),
            const Text(
              'Popular Destinations',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            destinations.when(
              loading: () => const Padding(
                padding: EdgeInsets.only(top: 60),
                child: Center(child: CircularProgressIndicator()),
              ),
              error: (error, _) => _ErrorState(
                message: error is Failure
                    ? error.message
                    : 'Something went wrong.',
                onRetry: () => ref.invalidate(destinationsProvider(_query)),
              ),
              data: (items) {
                if (items.isEmpty) {
                  return const _EmptyState();
                }
                return Column(
                  children: [
                    for (final d in items)
                      DestinationCard(
                        destination: d,
                        onTap: () => showDestinationDetailSheet(
                          context,
                          d,
                          onFindGuide: widget.onFindGuide,
                        ),
                      ),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _SearchField extends StatelessWidget {
  const _SearchField({required this.controller, required this.onSubmitted});

  final TextEditingController controller;
  final ValueChanged<String> onSubmitted;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      textInputAction: TextInputAction.search,
      onSubmitted: onSubmitted,
      decoration: InputDecoration(
        hintText: 'Where do you want to go?',
        prefixIcon: const Icon(Icons.location_on_outlined,
            color: AppColors.primary),
        suffixIcon: IconButton(
          icon: const Icon(Icons.search),
          onPressed: () => onSubmitted(controller.text),
        ),
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.only(top: 60),
      child: Center(
        child: Text(
          'No destinations found.',
          style: TextStyle(color: AppColors.textSecondary),
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
    return Padding(
      padding: const EdgeInsets.only(top: 60),
      child: Center(
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
    );
  }
}
