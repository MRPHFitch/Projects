import 'package:flutter/material.dart';

class CalculatorAppearance extends StatelessWidget {
  const CalculatorAppearance({super.key});

  @override
  Widget build(BuildContext context) {
    // Calculator button labels
    final buttons = [
      ['7', '8', '9', '÷'],
      ['4', '5', '6', '×'],
      ['1', '2', '3', '−'],
      ['0', '.', '=', '+'],
    ];

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.only(top: 32, bottom: 32), // Adjust as needed
        child: Center(
          child: Container(
            decoration: BoxDecoration(
              color: Colors.black,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(
                  color: Colors.black12,
                  blurRadius: 8,
                  offset: Offset(0, 4),
                ),
              ],
            ),
            width: double.infinity,
            child: Column(
              mainAxisSize: MainAxisSize.max, // Fill vertical space
              mainAxisAlignment: MainAxisAlignment
                  .center, // Or .start if you want content at the top
              children: [
                // Display area
                Container(
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.all(16),
                  margin: const EdgeInsets.only(bottom: 12),
                  width: 260,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(35),
                    border: Border.all(color: Colors.grey[300]!),
                  ),
                  child: Text(
                    '0',
                    style: TextStyle(
                      fontSize: 60,
                      color: Colors.black87,
                      fontWeight: FontWeight.w500,
                      letterSpacing: 2,
                    ),
                  ),
                ),
                // Calculator buttons
                ...buttons.map(
                  (row) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: row.map((label) {
                        final isOperator = '÷×−+=.'.contains(label);
                        return Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 6),
                          child: SizedBox(
                            width: 80,
                            height: 120,
                            child: ElevatedButton(
                              onPressed: null, // Non-functional
                              style: ElevatedButton.styleFrom(
                                backgroundColor: isOperator
                                    ? Colors.orange[300]
                                    : Colors.white,
                                foregroundColor: isOperator
                                    ? Colors.white
                                    : Colors.black87,
                                disabledBackgroundColor: isOperator
                                    ? Colors.orange[300]
                                    : Colors.white,
                                disabledForegroundColor: isOperator
                                    ? Colors.white
                                    : Colors.black87,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                elevation: 0,
                                side: BorderSide(color: Colors.grey[300]!),
                              ),
                              child: Text(
                                label,
                                style: TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
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
