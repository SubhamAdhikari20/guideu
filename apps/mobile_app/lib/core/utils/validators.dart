/// Simple, reusable form validators used across the auth screens.
class Validators {
  Validators._();

  static String? email(String? value) {
    if (value == null || value.trim().isEmpty) return 'Email is required';
    final re = RegExp(r'^[\w.\-]+@[\w\-]+\.[\w.\-]+$');
    return re.hasMatch(value.trim()) ? null : 'Enter a valid email';
  }

  static String? password(String? value) {
    if (value == null || value.isEmpty) return 'Password is required';
    return value.length >= 6 ? null : 'Password must be at least 6 characters';
  }

  static String? required(String? value, String field) {
    return (value == null || value.trim().isEmpty) ? '$field is required' : null;
  }
}
