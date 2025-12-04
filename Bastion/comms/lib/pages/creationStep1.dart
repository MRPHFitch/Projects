import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AccountCreationStep1 extends StatefulWidget {
  final void Function(String phoneNumber) onNext;
  const AccountCreationStep1({super.key, required this.onNext});

  @override
  State<AccountCreationStep1> createState() => _AccountCreationStep1State();
}

class _AccountCreationStep1State extends State<AccountCreationStep1> {
  final List<TextEditingController> _controllers =
      List.generate(9, (_) => TextEditingController());
  final List<FocusNode> _focusNodes = List.generate(9, (_) => FocusNode());

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
    if (value.length == 1 && idx < 8) {
      _focusNodes[idx + 1].requestFocus();
    }
    if (value.isEmpty && idx > 0) {
      _focusNodes[idx - 1].requestFocus();
    }
  }

  void _submit() {
    final phone = _controllers.map((c) => c.text).join();
    if (phone.length == 9 && phone.runes.every((r) => r >= 48 && r <= 57)) {
      widget.onNext(phone);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a 9-digit phone number.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Account'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Step 1', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 24),
            const Text(
              'Enter your 9-digit Phone Number',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(9, (idx) {
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
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
                        if (idx == 8) _submit();
                      },
                    ),
                  ),
                );
              }),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              onPressed: _submit,
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}