import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:comms/widgets/digitentry.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/treemanager.dart';

final KaryForest forest = KaryForest();

class AccountCreationStep2 extends StatefulWidget {
  final String username;
  final void Function(String badgeId) onComplete;
  final VoidCallback onBack;
  const AccountCreationStep2({
    super.key,
    required this.username,
    required this.onComplete,
    required this.onBack,
  });

  @override
  State<AccountCreationStep2> createState() => _AccountCreationStep2State();
}

class _AccountCreationStep2State extends State<AccountCreationStep2> {
  final _formKey = GlobalKey<FormState>();
  final _allClearController = TextEditingController();
  final _safeNotClearController = TextEditingController();
  final _notSafeController = TextEditingController();
  final _dangerController = TextEditingController();

  String? _badgeId;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _generateBadgeId();
  }

  @override
  void dispose() {
    _allClearController.dispose();
    _safeNotClearController.dispose();
    _notSafeController.dispose();
    _dangerController.dispose();
    super.dispose();
  }

  void _generateBadgeId() async {
    final response= await http.post(
      Uri.parse('https://backend.com/api/create-account'),
      body: {
        'username': widget.username,
      },
    );
    if(response.statusCode==200){
      setState(() {
        _badgeId=jsonDecode(response.body)['badgeId'];
      });
    }
  }

  bool _isSingleDigit(String? value) {
    return value != null && value.length == 1 && int.tryParse(value) != null;
  }

  Widget _digitEntry({
    required String label,
    required TextEditingController controller,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(label, textAlign: TextAlign.center, style: const TextStyle(fontSize: 16)),
        const SizedBox(height: 8),
        Center(
          child: SizedBox(
            width: 48,
            child: TextFormField(
              controller: controller,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, letterSpacing: 2),
              keyboardType: TextInputType.number,
              inputFormatters: [
                FilteringTextInputFormatter.digitsOnly,
                LengthLimitingTextInputFormatter(1),
              ],
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                isDense: true,
                contentPadding: EdgeInsets.symmetric(vertical: 12),
              ),
              validator: (value) =>
                _isSingleDigit(value) ? null : 'Enter 0-9',
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Account Created'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: widget.onBack,
        ),
      ),
      body: Center(
        child: _isLoading
            ? const CircularProgressIndicator()
            : SingleChildScrollView(
                padding: const EdgeInsets.all(24),
                child: Form(
                  key: _formKey,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // Prominent Badge #
                      const Text(
                        'Your Badge ID#',
                        style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        _badgeId ?? '',
                        style: const TextStyle(
                          fontSize: 40,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange,
                          letterSpacing: 2,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'Please save this Badge ID# for future logins.',
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 32),

                      // Digit entries, centered and styled
                      _digitEntry(
                        label: 'Choose a digit to indicate you are All Clear',
                        controller: _allClearController,
                      ),
                      const SizedBox(height: 20),
                      DigitEntryField(
                        label: 'Choose a different digit to indicate you are Safe but Not Clear',
                        controller: _safeNotClearController,
                      ),
                      const SizedBox(height: 20),
                      DigitEntryField(
                        label: 'Choose another different digit to indicate you are Not Safe, but don\'t need assistance',
                        controller: _notSafeController,
                      ),
                      const SizedBox(height: 20),
                      DigitEntryField(
                        label: 'Choose the last different digit to indicate you are in Immediate Danger and need assistance',
                        controller: _dangerController,
                      ),
                      const SizedBox(height: 24),
                      const Text('You will input one status code at the end of your Badge ID in order to login',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 16,
                        color: Colors.orange,
                        ),
                      ),
                      const SizedBox(height: 32),

                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: () {
                            if (_formKey.currentState!.validate()) {
                              // Save or process the digits as needed
                              widget.onComplete(_badgeId!);
                              Navigator.pushReplacementNamed(context, '/login');
                            }
                          },
                          
                          child: const Text('Continue'),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
      ),
    );
  }
}