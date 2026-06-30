import 'package:flutter/material.dart';

import 'routes/app_router.dart';
import 'theme/app_theme.dart';

/// Root widget for GuideU. Navigation is handled by GoRouter; the feature
/// shells are reached through [appRouter].
class GuideUApp extends StatelessWidget {
  const GuideUApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'GuideU',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      routerConfig: appRouter,
    );
  }
}
