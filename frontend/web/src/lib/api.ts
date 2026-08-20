import axios from 'axios';
import { ResearchRequest, ResearchResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateResearch = async (data: ResearchRequest): Promise<ResearchResponse> => {
  const response = await api.post<ResearchResponse>('/api/v1/research', data);
  return response.data;
};