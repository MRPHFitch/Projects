import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class LoginPage extends StatefulWidget {
  final void Function(String code, dynamic statusCode) onSubmit;
  const LoginPage({super.key, required this.onSubmit});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final List<TextEditingController> _controllers = List.generate(
    7,
    (_) => TextEditingController(),
  );
  final List<FocusNode> _focusNodes = List.generate(7, (_) => FocusNode());

  @override
  void dispose() {
    for (final c in _controllers) {
      c.dispose();
    }
    for (final f in _focusNodes) {
      f.dispose();
    }
    super.dispose();
  }

  void _onChanged(int idx, String value) {
    if (value.length == 1 && idx < 6) {
      _focusNodes[idx + 1].requestFocus();
    }
    if (value.isEmpty && idx > 0) {
      _focusNodes[idx - 1].requestFocus();
    }
  }

  void _submit() {
    final code = _controllers.map((c) => c.text).join();
    if (code.length == 7 && code.runes.every((r) => r >= 48 && r <= 57)) {
      final badgeId = code.substring(0, 6); // Parse Badge from status code
      final statusDigit = code.substring(6, 7);
      widget.onSubmit(badgeId, statusDigit);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter all 7 digits.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            const Text(
              'Enter your 7-digit Login Code',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(7, (idx) {
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 6),
                  child: SizedBox(
                    width: 44,
                    child: TextField(
                      controller: _controllers[idx],
                      focusNode: _focusNodes[idx],
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 24),
                      keyboardType: TextInputType.number,
                      inputFormatters: [
                        FilteringTextInputFormatter.digitsOnly,
                        LengthLimitingTextInputFormatter(1),
                      ],
                      onChanged: (val) => _onChanged(idx, val),
                      onSubmitted: (val) {
                        if (idx == 6) _submit();
                      },
                    ),
                  ),
                );
              }),
            ),
            const SizedBox(height: 32),
            ElevatedButton(onPressed: _submit, child: const Text('Login')),
          ],
        ),
      ),
    );
  }
}
