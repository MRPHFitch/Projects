import { WebSocketGateway, OnGatewayConnection, WebSocketServer, OnGatewayDisconnect } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { JwtService } from '@nestjs/jwt';
import { MessagesService } from '../messages/messages.service';

@WebSocketGateway({ cors: true })
export class MessagingGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server: Server;
  private socketsByUser = new Map<string, Set<string>>(); // userId -> socketIds
  private socketToDevice = new Map<string, string>(); // socketId -> deviceId

  constructor(private jwt: JwtService, private messages: MessagesService) {}

  async handleConnection(socket: Socket) {
    try {
      const token = socket.handshake.auth?.token;
      const payload = this.jwt.verify(token, { secret: process.env.JWT_SECRET });
      const userId = payload.sub;
      const deviceId = socket.handshake.auth.deviceId;

      // store mapping
      if (!this.socketsByUser.has(userId)) this.socketsByUser.set(userId, new Set());
      this.socketsByUser.get(userId).add(socket.id);
      if (deviceId) this.socketToDevice.set(socket.id, deviceId);

      // deliver queued messages for this device
      const queued = await this.messages.getQueuedMessagesForDevice(userId, deviceId);
      for (const msg of queued) {
        socket.emit('message', { id: msg.id, payload: msg.payload, fromUserId: msg.fromUserId, fromDevice: msg.fromDevice });
        // mark delivered
        await this.messages.markDelivered(msg.id);
      }
    } catch (err) {
      console.error('Socket handshake failed', err);
      socket.disconnect(true);
    }
  }

  handleDisconnect(socket: Socket) {
    // cleanup mappings
  }

  // helper to emit to recipient devices
  async emitToDevice(userId: string, deviceId: string, event: string, data: any) {
    // find socket(s) for userId/deviceId, emit
  }
}