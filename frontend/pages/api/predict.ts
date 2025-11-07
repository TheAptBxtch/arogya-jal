import type { NextApiRequest, NextApiResponse } from 'next';

interface SensorReading {
  vibration: number;
  current: number;
  temperature: number;
}

interface PredictionResponse {
  probability_of_failure: number;
  timestamp: string;
  status: string;
  confidence_level?: string;
  error?: string;
  detail?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<PredictionResponse>
) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).json({
      probability_of_failure: 0,
      timestamp: new Date().toISOString(),
      status: 'error',
      error: 'Method not allowed',
      detail: 'Only POST requests are supported'
    });
  }

  try {
    // Validate request body
    if (!req.body || typeof req.body !== 'object') {
      return res.status(400).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Invalid request body',
        detail: 'Request body must be a valid JSON object'
      });
    }

    const { vibration, current, temperature } = req.body as SensorReading;

    // Validate sensor readings
    if (typeof vibration !== 'number' || vibration < 0 || vibration > 10) {
      return res.status(422).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Validation error',
        detail: 'Vibration must be a number between 0 and 10'
      });
    }

    if (typeof current !== 'number' || current < 0 || current > 50) {
      return res.status(422).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Validation error',
        detail: 'Current must be a number between 0 and 50'
      });
    }

    if (typeof temperature !== 'number' || temperature < -20 || temperature > 150) {
      return res.status(422).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Validation error',
        detail: 'Temperature must be a number between -20 and 150'
      });
    }

    // Get backend API URL from environment variables
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const apiUrl = `${backendUrl}/api/predict`;

    console.log(`Forwarding request to: ${apiUrl}`);

    // Forward request to backend API
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'ArogyaJal-Frontend/1.0.0'
      },
      body: JSON.stringify({
        vibration,
        current,
        temperature
      }),
      // Add timeout to prevent hanging requests
      signal: AbortSignal.timeout(30000) // 30 second timeout
    });

    // Handle backend API errors
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Backend API error: ${response.status} - ${errorText}`);

      let errorDetail;
      try {
        const errorJson = JSON.parse(errorText);
        errorDetail = errorJson.detail || errorJson.error || 'Unknown backend error';
      } catch {
        errorDetail = errorText || 'Unknown backend error';
      }

      return res.status(response.status).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: `Backend API error (${response.status})`,
        detail: errorDetail
      });
    }

    // Parse and forward successful response
    const result = await response.json();

    // Validate response format
    if (typeof result.probability_of_failure !== 'number' ||
        typeof result.timestamp !== 'string' ||
        typeof result.status !== 'string') {
      console.error('Invalid response format from backend:', result);

      return res.status(502).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Invalid backend response',
        detail: 'Backend API returned an invalid response format'
      });
    }

    // Ensure probability is within valid range
    const probability = Math.max(0, Math.min(1, result.probability_of_failure));

    // Return successful response
    res.status(200).json({
      probability_of_failure: probability,
      timestamp: result.timestamp,
      status: result.status,
      confidence_level: result.confidence_level
    });

  } catch (error: any) {
    console.error('API proxy error:', error);

    // Handle different types of errors
    if (error.name === 'AbortError') {
      return res.status(504).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Request timeout',
        detail: 'Backend API request timed out after 30 seconds'
      });
    }

    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        probability_of_failure: 0,
        timestamp: new Date().toISOString(),
        status: 'error',
        error: 'Service unavailable',
        detail: 'Backend API is not running or not accessible'
      });
    }

    // Generic error
    return res.status(500).json({
      probability_of_failure: 0,
      timestamp: new Date().toISOString(),
      status: 'error',
      error: 'Internal server error',
      detail: error.message || 'An unexpected error occurred'
    });
  }
}