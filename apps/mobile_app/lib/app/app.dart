import 'package:flutter/material.dart';

import 'theme/app_theme.dart';

/// Root widget for GuideU.
///
/// Routing (GoRouter) and the feature shells are wired in with the features in
/// later sprints; Sprint 1 ships only the app shell + theme foundation.
class GuideUApp extends StatelessWidget {
  const GuideUApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GuideU',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      home: const _FoundationHome(),
    );
  }
}

class _FoundationHome extends StatelessWidget {
  const _FoundationHome();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('GuideU')),
      body: const Center(
        child: Text('GuideU mobile — foundation ready.'),
      ),
    );
  }
}
