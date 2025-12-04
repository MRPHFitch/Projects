import 'dart:convert';
import 'package:flutter/material.dart';
import 'creationStep1.dart';
import 'creationStep2.dart';

class DescriptionStep extends StatelessWidget{
    final VoidCallback onAccept;
    const DescriptionStep({super.key, required this.onAccept});

    @override
    Widget build(BuildContext context){
      const String headsUp='''
  Before continuing, this is a normal messaging app, but this creation is what makes it different. There will 
  be a couple of steps to complete for account creation. The first will be to provide a unique username. 
  This is how others will search for you in order to message you. The next step will ask you for some digits 
  to indicate a status. This is where the app is different. Every time you log in, you will need to provide 
  one of those status codes. The purpose of the status code is for you. The codes represent if you are in danger 
  or safe. If in danger, the app will ready your status code and send to the police a call for help including your 
  specific location, a short recording (5-10seconds) right after keying in the status and a picture of your 
  surroundings. That means the app will need access to your microphone and camera for normal messaging purposes, 
  but also to properly notify authorities if you need help. You will also be able to provide a security contact 
  that the information can be sent to in addition to authorities.

  The hope is that those suffering abuse, or being kidnapped, or being trafficked can get help without those 
  endangering them knowing. Those details will never be used unless your status code is input. Everything about 
  the app is to provide security and privacy for you. No personal information is stored, just the unique username 
  you provided.

  Do not forget your status codes

  If you would still like to continue, then we can't wait to show you the app.
  ''';
    return Scaffold(
      appBar: AppBar(title: const Text("Welcome")),
      body: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Padding(
        padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(headsUp,
              style: TextStyle(fontSize: 14,
                color: Colors.orange),
                softWrap: false,
              ), 
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: onAccept,
                child: const Text('Continue')
              ),
            ],
          )
        )
      )
    );
  }
}

class AccountCreationPage extends StatefulWidget {
  final VoidCallback onAccountCreated;
  const AccountCreationPage({super.key, required this.onAccountCreated});

  @override
  State<AccountCreationPage> createState() => _AccountCreationPageState();
}

class _AccountCreationPageState extends State<AccountCreationPage> {
  int _step = 0;
  String? phoneNumber;

  
  void _goToStep2(String phoneNum) {
    setState(() {
      phoneNumber=phoneNum;
      _step = 2;
    });
  }

  void _goBackToStep1() {
    setState(() {
      _step = 1;
    });
  }

  void _completeAccount(String phoneNumber) {
    // In P2P, just mark the account as created locally.
    widget.onAccountCreated();
    Navigator.pushReplacementNamed(context, '/login');
  }

  void _onPhoneEntered(String phone){
    setState(() {
      phoneNumber=phone;
    });
    _completeAccount(phoneNumber!);
  }

  @override
  Widget build(BuildContext context) {
    if(_step==0){
      return DescriptionStep(onAccept: ()=>setState(() =>_step=1));
    }
    else if (_step == 1) {
      return AccountCreationStep1(onNext: _goToStep2);
    } else {
      return AccountCreationStep2(
        username: phoneNumber!,
        onComplete: _onPhoneEntered,
        onBack: _goBackToStep1,
      );
    }
  }
}