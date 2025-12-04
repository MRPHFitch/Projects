import 'package:camera/camera.dart';
import 'package:comms/widgets/calc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_close_app/flutter_close_app.dart';
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

class EmergencyPage extends StatefulWidget {
  final CameraDescription camera;
  const EmergencyPage({super.key, required this.camera});

  @override
  State<EmergencyPage> createState() => _EmergencyPageState();
}


class _EmergencyPageState extends State<EmergencyPage> {
  bool _isProcessing = false;
  String? _result;

  @override
  void initState(){
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_){
      sendEmergencyMessage();
    });
  }

  Future<Map<String, dynamic>> recordVideoWithLocation(CameraDescription camera) async {
    final controller = CameraController(camera, ResolutionPreset.high);
    await controller.initialize();

    await controller.startVideoRecording();
    await Future.delayed(const Duration(seconds: 10));
    final file = await controller.stopVideoRecording();
    final position = await Geolocator.getCurrentPosition();
    await controller.dispose();

    return {
      'videoPath': file.path,
      'latitude': position.latitude,
      'longitude': position.longitude,
    };
  }

  Future<void> sendEmergencyMessage() async {
    setState(() {
      _isProcessing = true;
      _result = null;
    });

    // Double-check permissions in case user revoked them
    final cameraStatus = await Permission.camera.status;
    final micStatus = await Permission.microphone.status;
    final locStatus = await Permission.location.status;

    if (!cameraStatus.isGranted || !micStatus.isGranted || !locStatus.isGranted) {
      setState(() {
        _isProcessing = false;
        _result = 'Camera, microphone, and location permissions are required.';
      });
      return;
    }

    try {
      final data = await recordVideoWithLocation(widget.camera);

      // Example message structure
      final message = {
        'type': 'emergency_video',
        'videoPath': data['videoPath'],
        'latitude': data['latitude'],
        'longitude': data['longitude'],
        'timestamp': DateTime.now().toIso8601String(),
      };

      // TODO: Replace this with your actual message sending logic
      // await sendMessage(message);
      FlutterCloseApp.close;

      setState(() {
        _isProcessing = false;
        _result = 'Video saved: ${data['videoPath']}\n'
                  'Lat: ${data['latitude']}, Lon: ${data['longitude']}';
      });
    } catch (e) {
      setState(() {
        _isProcessing = false;
        _result = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CalculatorAppearance(),
    );
  }
}