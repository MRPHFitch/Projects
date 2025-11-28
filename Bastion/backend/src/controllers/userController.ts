import {Request, Response} from 'express';
import {BadgeService} from '../services/badgeService';
import crypto from 'crypto';

function hashUser(username: string):string{
    return crypto.createHash('sha256').update(username).digest('hex');
}

// Instantiate service (in real app, use dependency injection)
const badgeService = new BadgeService();

export class UserController {
  // POST /api/users/create
  static async createUser(req: Request, res: Response) {
    try {
      const {username} = req.body;
      if (!username) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      // Encode username and Badge ID as needed (hash/encrypt)
      const encodedUser=hashUser(username); // Replace with real encoding
      const badgeId=badgeService.insertAndGetBadge(encodedUser);
      const hashBadge=hashUser(badgeId);
      // TODO: Save user to database with badgeId and other info

      return res.status(201).json({ badgeId });
    }
    catch (err) {
      return res.status(500).json({ error: 'Internal server error' });
    }
  }
}