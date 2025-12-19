import 'package:comms/widgets/digitentry.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';


class AccountCreationStep2 extends StatefulWidget {
  final String username;
  final void Function(String phoneNumber) onComplete;
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

  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _isLoading=false;
  }

  @override
  void dispose() {
    _allClearController.dispose();
    super.dispose();
  }

  Future<void> saveStatusCode(String allClear) async{
    final pref=await SharedPreferences.getInstance();
    await pref.setString('Clear status code', allClear);
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
        centerTitle: true,
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
                      // Digit entries, centered and styled
                      _digitEntry(
                        label: 'Choose a digit to indicate you are All Clear',
                        controller: _allClearController,
                      ),
                      const SizedBox(height: 24),
                      const Text('You will input one digit in order to login. If safe, put the digit you chose, if in danger, put any other digit',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 16,
                        color: Colors.orange,
                        ),
                      ),
                      const SizedBox(height: 32),

                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: () async{
                            if (_formKey.currentState!.validate()) {
                              final allClear=_allClearController.text;
                              await saveStatusCode(allClear);
                              // Save or process the digits as needed
                              widget.onComplete(widget.username);
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