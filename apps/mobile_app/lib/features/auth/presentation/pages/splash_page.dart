import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/routes/app_router.dart';
import '../providers/auth_providers.dart';
import '../providers/auth_state.dart';
import '../widgets/guideu_logo.dart';

/// Shows the logo while restoring any saved session, then routes the user.
class SplashPage extends ConsumerStatefulWidget {
  const SplashPage({super.key});

  @override
  ConsumerState<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends ConsumerState<SplashPage> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(authControllerProvider.notifier).bootstrap());
  }

  @override
  Widget build(BuildContext context) {
    ref.listen<AuthState>(authControllerProvider, (previous, next) {
      if (next is AuthAuthenticated) {
        context.go(AppRoutes.home);
      } else if (next is AuthUnauthenticated || next is AuthFailure) {
        context.go(AppRoutes.login);
      }
    });

    return const Scaffold(
      body: Center(child: GuideULogo(height: 64)),
    );
  }
}
