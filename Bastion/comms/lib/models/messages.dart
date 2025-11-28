import 'package:flutter/material.dart';

enum MessageStatus{sending, sent, delivered, read, failed}

class Message{
  final String text;
  final bool isReceived;
  final String contact;   //Sender's  name or ID
  final Color? bubbleColor;
  final MessageStatus status;
  final DateTime timestamp;

  Message({
    required this.text,
    required this.isReceived,
    required this.contact,
    this.bubbleColor,
    this.status=MessageStatus.sending,
    DateTime? timestamp,
  }) : timestamp=timestamp??DateTime.now();
}