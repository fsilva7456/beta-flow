import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { workflowApi } from '../api/workflowApi';
import WorkflowList from '../components/WorkflowList';

function Home() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: workflows = [], isLoading, error } = useQuery(
    ['workflows'],
    workflowApi.getAllWorkflows
  );

  const executeMutation = useMutation(workflowApi.executeWorkflow, {
    onSuccess: (data, workflowId) => {
      navigate(`/results/${workflowId}`);
    },
  });

  const handleExecute = (workflowId) => {
    executeMutation.mutate(workflowId);
  };

  if (isLoading) {
    return <Typography>Loading workflows...</Typography>;
  }

  if (error) {
    return <Typography color="error">Error loading workflows: {error.message}</Typography>;
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
