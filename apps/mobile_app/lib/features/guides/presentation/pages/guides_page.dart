import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme/app_colors.dart';
import '../../../../core/error/failures.dart';
import '../providers/guide_providers.dart';
import '../widgets/guide_card.dart';
import '../widgets/guide_profile_sheet.dart';

/// Guides tab — search and browse verified guides ("Book Guides" prototype).
class GuidesPage extends ConsumerStatefulWidget {
  const GuidesPage({super.key});

  @override
  ConsumerState<GuidesPage> createState() => _GuidesPageState();
}

class _GuidesPageState extends ConsumerState<GuidesPage> {
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
    final guides = ref.watch(guidesProvider(_query));

    return Scaffold(
      appBar: AppBar(title: const Text('Guides')),
      body: RefreshIndicator(
        onRefresh: () => ref.refresh(guidesProvider(_query).future),
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
          children: [
            TextField(
              controller: _searchController,
              textInputAction: TextInputAction.search,
              onSubmitted: _onSearch,
              decoration: InputDecoration(
                hintText: 'Where do you need a guide?',
                prefixIcon: const Icon(Icons.location_on_outlined,
                    color: AppColors.primary),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.search),
                  onPressed: () => _onSearch(_searchController.text),
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'Available Guides',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            guides.when(
              loading: () => const Padding(
                padding: EdgeInsets.only(top: 60),
                child: Center(child: CircularProgressIndicator()),
              ),
              error: (error, _) => _ErrorState(
                message:
                    error is Failure ? error.message : 'Something went wrong.',
                onRetry: () => ref.invalidate(guidesProvider(_query)),
              ),
              data: (items) {
                if (items.isEmpty) {
                  return const Padding(
                    padding: EdgeInsets.only(top: 60),
                    child: Center(
                      child: Text(
                        'No guides found.',
                        style: TextStyle(color: AppColors.textSecondary),
                      ),
                    ),
                  );
                }
                return Column(
                  children: [
                    for (final g in items)
                      GuideCard(
                        guide: g,
                        onTap: () => showGuideProfileSheet(context, g),
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
