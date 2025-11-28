// // devices.controller.ts
// @Post('register')
// async registerDevice(@Req() req, @Body() dto) {
//   // create Device entry for req.user.id
// }

// @Post(':deviceId/prekeys')
// async uploadPrekeys(@Req() req, @Param('deviceId') deviceId, @Body() prekeysDto) {
//   // prekeysDto = [{keyId, publicKey}, ...]
//   // store prekeys in PreKey table
// }

// @Get(':userId/prekey-bundle')
// async getPrekeyBundle(@Param('userId') userId) {
//   // return one available signedPreKey + one-time prekey for target device
//   // mark one-time prekey used? Usually the initiator will mark as used after successful handshake
// }
