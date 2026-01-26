import 'package:hive/hive.dart';

class MessageStore {
  static Future<Box> openBox(String chatName) async {
    return await Hive.openBox('messages_$chatName');
  }

  static Future<List<Map>> loadMessages(Box box) async {
    final now = DateTime.now();
    final cutoff = now.subtract(Duration(days: 30));
    final allMessages = box.values.cast<Map>().toList();
    // Prune old messages
    for (var key in box.keys) {
      final msg = box.get(key);
      if (DateTime.parse(msg['timestamp']).isBefore(cutoff)) {
        box.delete(key);
      }
    }
    return allMessages.where((msg) {
      final ts = DateTime.parse(msg['timestamp']);
      return ts.isAfter(cutoff);
    }).toList();
  }

  static Future<void> addMessage(Box box, Map msg) async {
    await box.add(msg);
  }
}