import 'package:flutter/material.dart';
import 'package:hive/hive.dart';
import '../services/messageStorage.dart';

class ChatDetailPage extends StatefulWidget {
  final String chatName; // e.g., "Alice" or group name
  // Optionally pass chatId or other identifiers

  const ChatDetailPage({Key? key, required this.chatName}) : super(key: key);

  @override
  _ChatDetailPageState createState() => _ChatDetailPageState();
}

class _ChatDetailPageState extends State<ChatDetailPage> {
  final TextEditingController _controller = TextEditingController();
  late DateTime now;
  late DateTime cutoff;
  
  late Box messagesBox;
  List<Map> messages = [];
  

  @override
  void initState() {
    super.initState();
    setup();
  }

  Future<void> setup() async {
    messagesBox = await MessageStore.openBox(widget.chatName);
    messages = await MessageStore.loadMessages(messagesBox);
    setState(() {});
  }

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;
    final msg = {
      'sender': 'Me',
      'text': text,
      'timestamp': DateTime.now().toIso8601String(),
    };
    MessageStore.addMessage(messagesBox, msg);
    setState(() {
      messages.add(msg);
    });
    _controller.clear();
    // TODO: Send the message over the P2P channel here
  }

List<Map<String, dynamic>> pruneOldMessages(List<Map<String, dynamic>> messages) {
  return messages.where((msg) {
    final ts = DateTime.parse(msg['timestamp']);
    return ts.isAfter(cutoff);
  }).toList();
}

  // This function should be called when a message is received over P2P
  void onMessageReceived(String sender, String text) {
    setState(() {
      messages.add({'sender': sender, 'text': text});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.chatName),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final msg = messages[index];
                final isMe = msg['sender'] == 'Me';
                return Align(
                  alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 2),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: isMe ? Colors.blue[100] : Colors.grey[200],
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(msg['text'] ?? ''),
                  ),
                );
              },
            ),
          ),
          Divider(height: 1),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(),
                      isDense: true,
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}