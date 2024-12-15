import React from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Container, Typography, Button, Box, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { workflowApi } from '../api/workflowApi';
import WorkflowList from '../components/WorkflowList';

function Home() {
  console.log('Home component rendering');
  const navigate = useNavigate();

  const { data: workflows = [], isLoading, error } = useQuery(
    ['workflows'],
    async () => {
      console.log('Fetching workflows...');
      try {
        const result = await workflowApi.getAllWorkflows();
        console.log('Workflows fetched:', result);
        return result;
      } catch (error) {
        console.error('Error fetching workflows:', error);
        throw error;
      }
    }
  );

  const executeMutation = useMutation(
    async (workflowId) => {
      console.log('Executing workflow:', workflowId);
      return await workflowApi.executeWorkflow(workflowId);
    },
    {
      onSuccess: (data, workflowId) => {
        navigate(`/results/${workflowId}`);
      },
    }
  );

  const handleExecute = (workflowId) => {
    executeMutation.mutate(workflowId);
  };

  console.log('Current state:', { workflows, isLoading, error });

  if (isLoading) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Typography>Loading workflows...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error">
          Error loading workflows: {error.message}
          <br />
          {error.response?.data ? JSON.stringify(error.response.data) : 'No additional error details'}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Workflows
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/create')}
        >
          Create New Workflow
        </Button>
      </Box>
      <WorkflowList workflows={workflows} onExecute={handleExecute} />
    </Container>
  );
}

export default Home;