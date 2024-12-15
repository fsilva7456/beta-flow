import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const workflowApi = {
  getAllWorkflows: async () => {
    const response = await axios.get(`${API_URL}/api/v1/workflows`);
    return response.data;
  },

  getWorkflow: async (id) => {
    const response = await axios.get(`${API_URL}/api/v1/workflows/${id}`);
    return response.data;
  },

  createWorkflow: async (workflowData) => {
    const response = await axios.post(`${API_URL}/api/v1/workflows`, workflowData);
    return response.data;
  },

  executeWorkflow: async (id) => {
    const response = await axios.post(`${API_URL}/api/v1/workflows/${id}/execute`);
    return response.data;
  },
};
