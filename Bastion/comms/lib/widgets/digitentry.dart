import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class DigitEntryField extends StatelessWidget {
  final String label;
  final TextEditingController controller;

  const DigitEntryField({
    super.key,
    required this.label,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.bodyLarge,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 8),
        SizedBox(
          width: 48, // Just wide enough for one digit
          child: TextFormField(
            controller: controller,
            textAlign: TextAlign.center,
            keyboardType: TextInputType.number,
            inputFormatters: [
              FilteringTextInputFormatter.digitsOnly,
              LengthLimitingTextInputFormatter(1),
            ],
            style: const TextStyle(fontSize: 28),
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              isDense: true,
              contentPadding: EdgeInsets.symmetric(vertical: 12),
            ),
            validator: (value) =>
                value != null && value.length == 1 && int.tryParse(value) != null
                    ? null
                    : 'Enter 1 digit',
          ),
        ),
      ],
    );
  }
}