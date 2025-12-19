import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:comms/utils/platformCheck.dart';


class PermissionPage extends StatefulWidget {
  const PermissionPage({super.key});

  @override
  State<PermissionPage> createState() => _PermissionPageState();
}

class _PermissionPageState extends State<PermissionPage> {
  bool _checking = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (isDesktop || isWeb) {
      //If it isn't mobile, skip status code and jump to home page
      Navigator.pushReplacementNamed(context, '/home');
    }
    else{
      // Proceed with requesting permissions for mobile
      _requestPermissions();
    }
  }

  Future<void> _requestPermissions() async {
    final cameraStatus = await Permission.camera.request();
    final micStatus = await Permission.microphone.request();
    final loc=await Permission.location.request();

    if (cameraStatus.isGranted && micStatus.isGranted && loc.isGranted) {
      if (!mounted) return;
      Navigator.pushReplacementNamed(context, '/login');
    } else {
      setState(() {
        _checking = false;
        _error = 'Camera, microphone, and location permissions are required to continue.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Permissions Required')),
      body: Center(
        child: _checking
            ? Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Requesting permissions...'),
                ],
              )
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.warning, color: Colors.red, size: 48),
                  const SizedBox(height: 16),
                  Text(_error ?? '', textAlign: TextAlign.center, style: const TextStyle(color: Colors.red)),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: _requestPermissions,
                    child: const Text('Try Again'),
                  ),
                  const SizedBox(height: 8),
                  TextButton(
                    onPressed: () => openAppSettings(),
                    child: const Text('Open App Settings'),
                  ),
                ],
              ),
      ),
    );
  }
}