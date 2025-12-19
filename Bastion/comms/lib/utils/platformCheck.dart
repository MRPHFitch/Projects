// File: lib/utils/platform_info.dart
import 'package:flutter/foundation.dart' show defaultTargetPlatform, TargetPlatform, kIsWeb;

/// Returns true if the current platform is Android or iOS.
bool get isMobile => defaultTargetPlatform == TargetPlatform.android ||
                            defaultTargetPlatform == TargetPlatform.iOS;

/// Returns true if the current platform is Windows, macOS, or Linux.
bool get isDesktop => defaultTargetPlatform == TargetPlatform.windows ||
                             defaultTargetPlatform == TargetPlatform.macOS ||
                             defaultTargetPlatform == TargetPlatform.linux;

/// Returns true if the current platform is Web.
bool get isWeb => kIsWeb;