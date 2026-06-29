import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:guideu_mobile/app/app.dart';

void main() {
  testWidgets('GuideU app boots to the foundation home', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: GuideUApp()));
    expect(find.text('GuideU'), findsWidgets);
    expect(find.text('GuideU mobile — foundation ready.'), findsOneWidget);
  });
}
