import 'package:flutter/material.dart';
import 'chatDetail.dart';
import '../services/signal_service.dart';
import '../widgets/userSearch.dart';

class IndChats extends StatefulWidget {
  const IndChats({Key? key}) : super(key: key);

  @override
  State<IndChats> createState() => _IndChatsState();
}

class _IndChatsState extends State<IndChats> {
  // Example chat list
  final List<Map<String, String>> chats = [
    {'name': 'Alice', 'lastMessage': 'Hey!'},
    {'name': 'Bob', 'lastMessage': 'See you soon.'},
  ];

    Future<void> _startNewChat() async {
    String? selectedUser = await showDialog<String>(
      context: context,
      builder: (context) => UserSearchDialog(),
    );

    if (selectedUser != null && selectedUser.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ChatDetailPage(chatName: selectedUser),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Individual Chats'),
        actions: [
          IconButton(
            icon: Icon(Icons.chat),
            tooltip: 'Start New Chat',
            onPressed: _startNewChat,
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: chats.length,
        itemBuilder: (context, index) {
          final chat = chats[index];
          return ListTile(
            title: Text(chat['name'] ?? 'Unknown'),
            subtitle: Text(chat['lastMessage'] ?? ''),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatDetailPage(chatName: chat['name'] ?? 'Unknown'),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _startNewChat,
        child: Icon(Icons.chat),
        tooltip: 'Start New Chat',
      ),
    );
  }
}