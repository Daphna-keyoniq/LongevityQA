import { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    const { question } = req.body;
    res.status(200).json({ answer: `You asked: ${question}` });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}