import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/utils/validators.dart';
import '../widgets/auth_text_field.dart';

/// Collects an email to start password recovery. The reset email is wired to a
/// Celery task on the backend in a later sprint; for now it confirms the request.
class ForgotPasswordPage extends StatefulWidget {
  const ForgotPasswordPage({super.key});

  @override
  State<ForgotPasswordPage> createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  final _formKey = GlobalKey<FormState>();
  final _email = TextEditingController();

  @override
  void dispose() {
    _email.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState?.validate() ?? false) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('If an account exists for that email, a reset link will be sent.'),
        ),
      );
      context.pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Forgot password')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Enter the email linked to your account and we will send you a link to reset your password.',
                ),
                const SizedBox(height: 24),
                AuthTextField(
                  controller: _email,
                  hint: 'Email',
                  keyboardType: TextInputType.emailAddress,
                  validator: Validators.email,
                  textInputAction: TextInputAction.done,
                ),
                const SizedBox(height: 24),
                ElevatedButton(onPressed: _submit, child: const Text('Send reset link')),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
