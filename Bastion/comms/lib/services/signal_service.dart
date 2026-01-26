class SignalService {
  // Example using HTTP; adapt if using WebSocket
  static Future<List<String>> searchUsers(String query) async {
    // TODO: Replace with your actual API/WebSocket call to signalServer.py
    // Example HTTP GET: http://yourserver:8080/search?query=alice
    // For now, return dummy data:
    await Future.delayed(Duration(milliseconds: 300)); // Simulate network delay
    if (query.isEmpty) return [];
    // Replace with actual server response
    return ['Alice', 'Alicia', 'Alina'].where((u) => u.toLowerCase().contains(query.toLowerCase())).toList();
  }
}