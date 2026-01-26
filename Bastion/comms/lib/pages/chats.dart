import 'package:comms/pages/indChats.dart';
import 'package:flutter/material.dart';

class ChatPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: Text('Chats'),
          centerTitle: true,
          bottom: TabBar(
            tabs: [
              Tab(text: 'Individual'),
              Tab(text: 'Group'),
            ],
          ),
          actions: [
            IconButton(
              onPressed: null,
              icon: Icon(Icons.add)),
          ],
        ),
        body: TabBarView(
          children: [
            IndChats(),
            Center(child: Text('Group Chats')),      // Replace with your widget
          ],
        ),
      ),
    );
  }
}