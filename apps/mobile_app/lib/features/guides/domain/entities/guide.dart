/// Pure domain entity for a verified guide, mapped from the core-engine
/// `GuideRegistry` (Nepal's NTB licensing registry). No Flutter or JSON here.
class Guide {
  const Guide({
    required this.id,
    required this.externalId,
    required this.guideCode,
    required this.ntbLicenseNo,
    required this.certification,
    required this.languages,
    required this.regions,
    required this.yearsExperience,
    required this.averageRating,
    required this.totalTripsCompleted,
    required this.verificationStatus,
    required this.isVerified,
  });

  final int id;
  final String externalId;
  final String guideCode;
  final String ntbLicenseNo;
  final String certification;
  final List<String> languages;
  final List<String> regions;
  final double yearsExperience;
  final double averageRating;
  final int totalTripsCompleted;
  final String verificationStatus;
  final bool isVerified;

  String get ratingLabel => averageRating.toStringAsFixed(1);

  String get experienceLabel {
    final whole = yearsExperience == yearsExperience.roundToDouble();
    final value =
        whole ? yearsExperience.toInt().toString() : yearsExperience.toStringAsFixed(1);
    return '$value yrs exp';
  }
}
