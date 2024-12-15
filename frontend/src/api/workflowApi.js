import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'https://beta-flow-production.up.railway.app';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for debugging
api.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response.data;
  },
  error => {
    console.error('API Error:', error.response || error);
    throw error;
  }
);

export const workflowApi = {
  getAllWorkflows: async () => {
    console.log('Calling getAllWorkflows');
    const response = await api.get('/api/v1/workflows');
    return response;
  },

  getWorkflow: async (id) => {
    console.log(`Calling getWorkflow(${id})`);
    const response = await api.get(`/api/v1/workflows/${id}`);
    return response;
  },

  createWorkflow: async (workflowData) => {
    console.log('Calling createWorkflow with data:', workflowData);
    const response = await api.post('/api/v1/workflows', workflowData);
    return response;
  },

  updateWorkflow: async (id, workflowData) => {
    console.log(`Calling updateWorkflow(${id}) with data:`, workflowData);
    const response = await api.put(`/api/v1/workflows/${id}`, workflowData);
    return response;
  },

  executeWorkflow: async (id) => {
    console.log(`Calling executeWorkflow(${id})`);
    const response = await api.post(`/api/v1/workflows/${id}/execute`);
    return response;
  },
};
