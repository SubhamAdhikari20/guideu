import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/theme/app_colors.dart';
import '../../../auth/presentation/providers/auth_providers.dart';
import '../../../auth/presentation/providers/auth_state.dart';
import '../../../bookings/presentation/pages/packages_page.dart';
import '../../../guides/domain/entities/guide.dart';
import '../../../guides/presentation/providers/guide_providers.dart';
import '../../../guides/presentation/widgets/guide_profile_sheet.dart';

/// Home tab — discovery landing styled after the Home prototype: greeting,
/// search, a hero banner, quick actions and a "Nearby Guides" strip.
class HomePage extends ConsumerWidget {
  const HomePage({this.onSeeExplore, this.onSeeGuides, super.key});

  final VoidCallback? onSeeExplore;
  final VoidCallback? onSeeGuides;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(authControllerProvider);
    final name = state is AuthAuthenticated
        ? state.user.fullName.split(' ').first
        : 'traveller';
    final nearbyGuides = ref.watch(guidesProvider(''));

    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
          children: [
            _Header(name: name),
            const SizedBox(height: 16),
            _SearchBar(onTap: onSeeExplore),
            const SizedBox(height: 16),
            const _HeroBanner(),
            const SizedBox(height: 20),
            _QuickActions(onGuides: onSeeGuides),
            const SizedBox(height: 20),
            _PackagesCta(
              onTap: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const PackagesPage()),
              ),
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                const Text(
                  'Nearby Guides',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const Spacer(),
                TextButton(
                  onPressed: onSeeGuides,
                  child: const Text('See all'),
                ),
              ],
            ),
            const SizedBox(height: 4),
            SizedBox(
              height: 150,
              child: nearbyGuides.when(
                loading: () =>
                    const Center(child: CircularProgressIndicator()),
                error: (_, _) => const Center(
                  child: Text(
                    'Could not load guides.',
                    style: TextStyle(color: AppColors.textSecondary),
                  ),
                ),
                data: (guides) {
                  if (guides.isEmpty) {
                    return const Center(
                      child: Text(
                        'No guides yet.',
                        style: TextStyle(color: AppColors.textSecondary),
                      ),
                    );
                  }
                  final preview = guides.take(6).toList();
                  return ListView.separated(
                    scrollDirection: Axis.horizontal,
                    itemCount: preview.length,
                    separatorBuilder: (_, _) => const SizedBox(width: 12),
                    itemBuilder: (context, i) => _NearbyGuideCard(
                      guide: preview[i],
                      onTap: () => showGuideProfileSheet(context, preview[i]),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Header extends StatelessWidget {
  const _Header({required this.name});

  final String name;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Namaste, $name 👋',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 2),
            Row(
              children: const [
                Icon(Icons.location_on, size: 14, color: AppColors.primary),
                SizedBox(width: 2),
                Text(
                  'Kathmandu, Nepal',
                  style:
                      TextStyle(color: AppColors.textSecondary, fontSize: 13),
                ),
              ],
            ),
          ],
        ),
        const Spacer(),
        IconButton(
          icon: const Icon(Icons.notifications_none),
          onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Notifications are coming soon.')),
          ),
        ),
      ],
    );
  }
}

class _SearchBar extends StatelessWidget {
  const _SearchBar({this.onTap});

  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: AppColors.inputFill,
          borderRadius: BorderRadius.circular(14),
        ),
        child: Row(
          children: const [
            Icon(Icons.search, color: AppColors.textSecondary),
            SizedBox(width: 10),
            Text(
              'Explore destinations',
              style: TextStyle(color: AppColors.textSecondary),
            ),
          ],
        ),
      ),
    );
  }
}

class _HeroBanner extends StatelessWidget {
  const _HeroBanner();

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 150,
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppColors.primary, AppColors.primaryDark],
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const [
          Text(
            'Discover Nepal',
            style: TextStyle(
              color: Colors.white,
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 4),
          Text(
            'Experience the beauty of the Himalayas',
            style: TextStyle(color: Colors.white70),
          ),
        ],
      ),
    );
  }
}

class _QuickActions extends StatelessWidget {
  const _QuickActions({this.onGuides});

  final VoidCallback? onGuides;

  @override
  Widget build(BuildContext context) {
    void soon(String label) => ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$label booking is coming soon.')),
        );

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        _ActionItem(
          icon: Icons.hiking,
          label: 'Guides',
          onTap: onGuides ?? () {},
        ),
        _ActionItem(
          icon: Icons.hotel,
          label: 'Hotels',
          onTap: () => soon('Hotel'),
        ),
        _ActionItem(
          icon: Icons.flight,
          label: 'Flights',
          onTap: () => soon('Flight'),
        ),
        _ActionItem(
          icon: Icons.directions_bus,
          label: 'Buses',
          onTap: () => soon('Bus'),
        ),
      ],
    );
  }
}

class _ActionItem extends StatelessWidget {
  const _ActionItem({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  final IconData icon;
  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Column(
        children: [
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: AppColors.primary.withValues(alpha: 0.10),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Icon(icon, color: AppColors.primary, size: 28),
          ),
          const SizedBox(height: 6),
          Text(label, style: const TextStyle(fontSize: 13)),
        ],
      ),
    );
  }
}

class _PackagesCta extends StatelessWidget {
  const _PackagesCta({required this.onTap});

  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.gold.withValues(alpha: 0.14),
          borderRadius: BorderRadius.circular(14),
        ),
        child: Row(
          children: [
            const Icon(Icons.card_travel, color: AppColors.gold),
            const SizedBox(width: 12),
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Tour Packages',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                  SizedBox(height: 2),
                  Text(
                    'Book curated treks and tours across Nepal',
                    style:
                        TextStyle(color: AppColors.textSecondary, fontSize: 12.5),
                  ),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: AppColors.textSecondary),
          ],
        ),
      ),
    );
  }
}

class _NearbyGuideCard extends StatelessWidget {
  const _NearbyGuideCard({required this.guide, required this.onTap});

  final Guide guide;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 160,
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.border),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: LinearGradient(
                      colors: [AppColors.primary, AppColors.primaryDark],
                    ),
                  ),
                  child: const Icon(Icons.person, color: Colors.white, size: 22),
                ),
                const Spacer(),
                if (guide.isVerified)
                  const Icon(Icons.verified,
                      size: 16, color: AppColors.primary),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              guide.guideCode,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 2),
            Text(
              guide.certification,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                color: AppColors.textSecondary,
                fontSize: 12,
              ),
            ),
            const Spacer(),
            Row(
              children: [
                const Icon(Icons.star, size: 14, color: AppColors.gold),
                const SizedBox(width: 3),
                Text(
                  guide.ratingLabel,
                  style: const TextStyle(
                    fontSize: 12.5,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
