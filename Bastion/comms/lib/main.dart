import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'themes.dart';
import 'models/messages.dart';
import 'widgets/threedots.dart';
import 'pages/accountCreation.dart';
import 'pages/login.dart';
import 'pages/home.dart';
import 'pages/chats.dart';
import 'pages/video.dart';
import 'pages/burst.dart';

void main() {
  runApp(const BastionApp());
}

class BastionApp extends StatefulWidget {
  const BastionApp({super.key});
  @override
  BastionAppState createState()=>BastionAppState();
}
class BastionAppState extends State<BastionApp>{
  //Allow use of Dark mode
  ThemeMode theMode=ThemeMode.system;
  bool isCreated=false;

  //Allow toggling of dark mode
  void toggleTheme(){
    setState((){
      theMode=theMode==ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Bastion',
      theme: lightTheme,
      darkTheme: darkTheme,
      themeMode: theMode,
      initialRoute: isCreated?'/login':'/account',
      routes: {
        '/account': (context)=>AccountCreationPage(onAccountCreated: (){
          setState(() {
            isCreated=true;
          });
        }),
        '/login': (context) => LoginPage(
          onSubmit: (badgeId, statusDigit) async {
            final response=await http.post(
              Uri.parse('https://bastion.com/api/login'),
              headers: {'Content Type':' application/json'},
              body: jsonEncode({'badgeID':badgeId, 'statusCode': statusDigit,}),
            );
            if(response.statusCode==200){
              Navigator.pushReplacementNamed(context, '/home');
            }
          },
        ),
        '/home': (context)=>HomePage(toggleTheme: toggleTheme),
        '/chats': (context)=>ChatPage(),
        '/video': (context)=>VideoPage(),
        '/burst': (content)=>BurstPage(),
      },
      home: ChatHomeScreen(toggleTheme: toggleTheme),
    );
  }
}

class ChatHomeScreen extends StatefulWidget {
  final VoidCallback toggleTheme;
  const ChatHomeScreen({super.key, required this.toggleTheme});

  @override
  State<ChatHomeScreen> createState() => _ChatHomeScreenState();
}

class _ChatHomeScreenState extends State<ChatHomeScreen> {
  //Set up variables for controlling receipt of message, scrolling, and typing bubble
  final TextEditingController _controller = TextEditingController();
  final List<Message> _messages = [];
  final ScrollController scroller=ScrollController();
  final Map<String, Color> contactColors={};
  bool canSend=false;
  bool isTyping=false;
  final List<Color> availColors=[
    Colors.blue,
    Colors.green,
    Colors.orange,
    Color(0xFFFF00FF),
    Colors.cyan,
    Colors.teal,
    Colors.purple,
    Colors.yellow,
    Colors.pink,
    Colors.brown,
  ];

  Color getContactColor(String contact){
    if(!contactColors.containsKey(contact)){
      contactColors[contact]=availColors[contactColors.length % availColors.length];
    }
    return contactColors[contact]!;
  }



  @override
  //Establish that you can't send a message with no text in the field
  void initState(){
    super.initState();
    //Listen to changes in text field
    _controller.addListener((){
      setState((){
        canSend=_controller.text.trim().isNotEmpty;
        isTyping=_controller.text.trim().isNotEmpty;
      });
    });
    //Only autoscroll if User isn't reading prior messages.
    scroller.addListener((){
      final atBottom=scroller.offset>=scroller.position.maxScrollExtent-20;
    });
  }
  

  void _sendMessage() {
    final text = _controller.text.trim();
    if (!canSend) return;   //Safety Check
    setState(() {
      _messages.add(Message(
        text:text, 
        isReceived:false,
        contact: "Me",
        status: MessageStatus.sent,
        ));
    });
    _controller.clear();
    scrollToBottom();
  }

  void _receiveMessage(String text, String senderName){
    setState((){
      _messages.add(Message(text:text,
      isReceived:true,
      contact: senderName,
      status: MessageStatus.delivered,
      ));
    });
    scrollToBottom();
  }

  void updateMessageStatus(int index, MessageStatus newStatus){
    final oldMessage=_messages[index];
    setState((){
      _messages[index]=Message(
        text: oldMessage.text,
        isReceived: oldMessage.isReceived,
        contact: oldMessage.contact,
        status: newStatus,
        timestamp: oldMessage.timestamp,
      );
    });
  }
  //Auto-scroll to the bottom with new messages
  void scrollToBottom(){
    WidgetsBinding.instance.addPostFrameCallback((_){
      if(scroller.hasClients){
        scroller.animateTo(scroller.position.maxScrollExtent, 
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
        );
      }
    });
  }

  //Determine what color the message bubble should be based off of delivery status
  Color getBubbleColor(Message message, BuildContext context){
    final baseColor= message.isReceived
        ? getContactColor(message.contact)
        : Theme.of(context).colorScheme.primary;

    //Adjust depending on sent status
    switch(message.status){
      case MessageStatus.sending:
        return Colors.grey;
      case MessageStatus.sent:
        return Colors.blueGrey;
      case MessageStatus.delivered:
        return baseColor.withAlpha((.6*255).round());
      case MessageStatus.read:
        return baseColor;
      case MessageStatus.failed:
        return Colors.red;
    }
  }

  Color getTextColor(BuildContext context){
    return Theme.of(context).textTheme.bodyMedium!.color!;
  }

  //Render the message bubble
 Widget messageBubble(Message message) {
  final color = getBubbleColor(message, context);
  final textColor = Theme.of(context).textTheme.bodyMedium!.color;

  // Build the avatar widget
  Widget avatar=CircleAvatar(
    radius: 16,
    backgroundColor: getContactColor(message.contact),
    child: Text(
      message.contact.isNotEmpty ? message.contact[0] : '?', // first letter
      style: const TextStyle(color: Colors.white, fontSize: 16),
    ),
  );

  // Message content with sender name and timestamp
  Widget messageContent = Column(
    crossAxisAlignment:
        message.isReceived ? CrossAxisAlignment.start : CrossAxisAlignment.end,
    children: [
      if (message.isReceived)
        Text(
          message.contact,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: Colors.grey[600],
          ),
        ),
      const SizedBox(height: 2),
      Container(
        margin: const EdgeInsets.symmetric(vertical: 2),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(
          message.text,
          style: TextStyle(fontSize: 16, color: textColor),
        ),
      ),
      const SizedBox(height: 2),
      Text(
        formatTime(message.timestamp),
        style: TextStyle(fontSize: 10, color: Colors.grey[500]),
      ),
    ],
  );

  // Layout row with avatar and message
  return Padding(
    padding: const EdgeInsets.symmetric(vertical: 4),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment:
          message.isReceived ? MainAxisAlignment.start : MainAxisAlignment.end,
      children: message.isReceived
          ? [avatar, const SizedBox(width: 8), Expanded(child: messageContent)]
          : [Expanded(child: messageContent)],
    ),
  );
}


  //Format DTG correctly
  String formatTime(DateTime time){
    final now=DateTime.now();
    if(time.day==now.day && time.month==now.month && time.year==now.year){
      return "${time.hour.toString().padLeft(2,'0')}:${time.minute.toString().padLeft(2,'0')}";
    }
    else{
      return "${time.month}/${time.day} ${time.hour.toString().padLeft(2,'0')}:${time.minute.toString().padLeft(2,'0')}";
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Bastion Secure Chat"),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.brightness_6),
            onPressed:widget.toggleTheme,
          )
        ]
      ),
      body: Column(
        children: [
          //Message Display information
          Expanded(
            child: ListView.builder(
              controller: scroller,
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                return messageBubble(_messages[index]);
              },
            ),
          ),

          //Indicator for if other person is typing
          if(isTyping) const TypingIndicator(),
            // Padding(
            //   padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 4),
            //   child: Align(
            //     alignment: Alignment.centerLeft,
            //     child: Container(
            //       padding: const EdgeInsets.symmetric(horizontal:12.0, vertical:6),
            //       decoration: BoxDecoration(
            //         color: Theme.of(context).colorScheme.tertiary,
            //         borderRadius: BorderRadius.circular(12),
            //       ),
            //       child: Text(
            //         "User is Typing...",
            //         style: TextStyle(
            //           fontStyle: FontStyle.italic,
            //           fontSize: 14,
            //           color: Colors.white70,
            //         ),
            //       ),
            //     ),
            //   ),
            // ),

          //Input Area
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      decoration: const InputDecoration(
                        hintText: "Type your message...",
                        border: OutlineInputBorder(),
                      ),
                      onSubmitted: (_)=>_sendMessage(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    icon: const Icon(Icons.send),
                    color: canSend
                        ? Colors.orange
                        : Colors.grey,
                    onPressed: canSend ? _sendMessage : null,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
