/// Result of the "is this price fair?" check, mapped from the core-engine
/// `trust/price-check` response. Pure domain — no Flutter or JSON here.
class PriceCheckResult {
  const PriceCheckResult({
    required this.serviceType,
    required this.region,
    required this.season,
    required this.quotedPriceNpr,
    required this.benchmarkPriceNpr,
    required this.overchargeRatio,
    required this.isLikelyScam,
    required this.severity,
    required this.scamProbability,
    required this.source,
    required this.explanation,
  });

  final String serviceType;
  final String? region;
  final String? season;
  final int quotedPriceNpr;
  final int? benchmarkPriceNpr;
  final double? overchargeRatio;
  final bool isLikelyScam;
  final String? severity;
  final double? scamProbability;
  final String source; // "ml" | "benchmark" | ...
  final List<String> explanation;

  /// How far above (or below) the fair price, e.g. "+45%". Null when unknown.
  String? get deviationLabel {
    if (overchargeRatio == null) return null;
    final pct = ((overchargeRatio! - 1) * 100).round();
    return pct >= 0 ? '+$pct%' : '$pct%';
  }
}
