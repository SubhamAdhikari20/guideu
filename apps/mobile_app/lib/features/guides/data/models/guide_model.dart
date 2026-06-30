import '../../domain/entities/guide.dart';

/// Maps the core-engine `GuideRegistry` JSON to a [Guide] entity.
class GuideModel {
  const GuideModel({
    required this.id,
    required this.externalId,
    required this.guideCode,
    required this.ntbLicenseNo,
    required this.certification,
    required this.languageList,
    required this.regionList,
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
  final List<String> languageList;
  final List<String> regionList;
  final double yearsExperience;
  final double averageRating;
  final int totalTripsCompleted;
  final String verificationStatus;
  final bool isVerified;

  factory GuideModel.fromJson(Map<String, dynamic> json) {
    return GuideModel(
      id: json['id'] as int,
      externalId: (json['external_id'] ?? '') as String,
      guideCode: (json['guide_code'] ?? '') as String,
      ntbLicenseNo: (json['ntb_license_no'] ?? '') as String,
      certification: (json['certification'] ?? '') as String,
      languageList: _stringList(json['language_list']),
      regionList: _stringList(json['region_list']),
      yearsExperience: _toDouble(json['years_experience']),
      averageRating: _toDouble(json['average_rating']),
      totalTripsCompleted: (json['total_trips_completed'] ?? 0) as int,
      verificationStatus: (json['verification_status'] ?? '') as String,
      isVerified: (json['is_verified'] ?? false) as bool,
    );
  }

  static List<String> _stringList(dynamic value) {
    if (value is List) {
      return value.map((e) => e.toString()).toList();
    }
    return const [];
  }

  static double _toDouble(dynamic value) {
    if (value is num) return value.toDouble();
    if (value is String) return double.tryParse(value) ?? 0;
    return 0;
  }

  Guide toEntity() {
    return Guide(
      id: id,
      externalId: externalId,
      guideCode: guideCode,
      ntbLicenseNo: ntbLicenseNo,
      certification: certification,
      languages: languageList,
      regions: regionList,
      yearsExperience: yearsExperience,
      averageRating: averageRating,
      totalTripsCompleted: totalTripsCompleted,
      verificationStatus: verificationStatus,
      isVerified: isVerified,
    );
  }
}
