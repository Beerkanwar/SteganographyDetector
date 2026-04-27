const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface EncryptResponse {
  key: string;
  stego_image: string;
  capacity_bytes: number;
  payload_size_bytes: number;
  utilization_percent: number;
}

export interface DecryptResponse {
  plaintext: string;
}

export interface DetectResponse {
  label: 'clean' | 'stego';
  confidence: number;
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = 'API Request failed';
    try {
      const data = await res.json();
      message = data.detail || message;
    } catch (e) {
      // Ignored
    }
    throw new ApiError(res.status, message);
  }
  return res.json();
}

export const api = {
  encrypt: async (image: File, plaintext: string): Promise<EncryptResponse> => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('plaintext', plaintext);
    
    const res = await fetch(`${API_URL}/encrypt`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<EncryptResponse>(res);
  },

  decrypt: async (image: File, key: string): Promise<DecryptResponse> => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('key', key);
    
    const res = await fetch(`${API_URL}/decrypt`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<DecryptResponse>(res);
  },

  detect: async (image: File): Promise<DetectResponse> => {
    const formData = new FormData();
    formData.append('image', image);
    
    const res = await fetch(`${API_URL}/detect`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<DetectResponse>(res);
  }
};
