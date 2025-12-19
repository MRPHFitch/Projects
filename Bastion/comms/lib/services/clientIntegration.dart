import 'package:socket_io_client/socket_io_client.dart' as IO;
// Or use web_socket_channel for generic WebSockets

class SignalingService {
  late IO.Socket socket;

  SignalingService() {
    socket = IO.io('http://0.0.0.0:3000', <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': false,
    });
    socket.connect();

    socket.onConnect((_) {
      print('Connected to signaling server');
      socket.emit('register', 'your_phone_number_or_id'); // Register your client
    });

    socket.on('signal', (data) {
      // Handle incoming signaling messages (offer, answer, ice-candidate)
      // Pass these to your WebRTC peer connection
      print('Received signal: $data');
    });

    socket.onDisconnect((_) => print('Disconnected from signaling server'));
  }

  void sendSignal(String toUserId, String type, dynamic payload) {
    socket.emit('signal', {
      'to': toUserId,
      'type': type,
      'payload': payload,
    });
  }

  // Example: send SDP offer
  void sendSdpOffer(String toUserId, String sdp) {
    sendSignal(toUserId, 'offer', {'sdp': sdp, 'type': 'offer'});
  }

  // Example: send ICE candidate
  void sendIceCandidate(String toUserId, String sdpMid, int sdpMLineIndex, String candidate) {
    sendSignal(toUserId, 'ice-candidate', {
      'sdpMid': sdpMid,
      'sdpMLineIndex': sdpMLineIndex,
      'candidate': candidate,
    });
  }
}