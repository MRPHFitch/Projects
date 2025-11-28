import 'package:flutter/material.dart';

class AccountCreationStep1 extends StatefulWidget {
  final void Function(String username) onNext;
  const AccountCreationStep1({super.key, required this.onNext});

  @override
  State<AccountCreationStep1> createState() => _AccountCreationStep1State();
}

class _AccountCreationStep1State extends State<AccountCreationStep1> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();

  @override
  void dispose() {
    _usernameController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      widget.onNext(
        _usernameController.text.trim()
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
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Step 1', style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 24),
              TextFormField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(),
                ),
                validator: (value) =>
                  value == null || value.isEmpty ? 'Enter your unique Username' : null,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _submit,
                child: const Text('Next'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}