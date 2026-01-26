import 'package:flutter/material.dart';
import '../services/signal_service.dart';

class UserSearchDialog extends StatefulWidget {
  @override
  _UserSearchDialogState createState() => _UserSearchDialogState();
}

class _UserSearchDialogState extends State<UserSearchDialog> {
  String query = '';
  List<String> results = [];
  bool isLoading = false;

  void _searchUsers(String input) async {
    setState(() {
      isLoading = true;
      query = input;
    });
    // Replace with your actual signal server search call
    final found = await SignalService.searchUsers(input);
    setState(() {
      results = found;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Search for User'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            autofocus: true,
            decoration: InputDecoration(hintText: 'Enter username'),
            onChanged: _searchUsers,
          ),
          if (isLoading) CircularProgressIndicator(),
          if (!isLoading)
            ...results.map((user) => ListTile(
                  title: Text(user),
                  onTap: () => Navigator.of(context).pop(user),
                )),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: Text('Cancel'),
        ),
      ],
    );
  }
}