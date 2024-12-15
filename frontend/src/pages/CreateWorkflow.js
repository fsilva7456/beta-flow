import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  TextField,
  Box,
  Alert,
} from '@mui/material';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import WorkflowStepForm from '../components/WorkflowStepForm';
import { workflowApi } from '../api/workflowApi';

function CreateWorkflow() {
  const navigate = useNavigate();
  const [workflowName, setWorkflowName] = useState('');
  const [steps, setSteps] = useState([]);
  const [error, setError] = useState('');

  const createMutation = useMutation(workflowApi.createWorkflow, {
    onSuccess: () => {
      navigate('/');
    },
    onError: (error) => {
      setError(error.message);
    },
  });

  const handleAddStep = () => {
    setSteps([
      ...steps,
      {
        step_name: '',
        action: 'llm-call',
        parameters: {
          prompt: '',
          model: 'gpt-4-turbo',
        },
      },
    ]);
  };

  const handleUpdateStep = (index, updatedStep) => {
    const newSteps = [...steps];
    newSteps[index] = updatedStep;
    setSteps(newSteps);
  };

  const handleDeleteStep = (index) => {
    const newSteps = steps.filter((_, i) => i !== index);
    setSteps(newSteps);
  };

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const items = Array.from(steps);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setSteps(items);
  };

  const handleSubmit = () => {
    if (!workflowName) {
      setError('Workflow name is required');
      return;
    }

    if (steps.length === 0) {
      setError('At least one step is required');
      return;
    }

    createMutation.mutate({
      workflow_name: workflowName,
      steps: steps,
    });
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Create Workflow
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TextField
        fullWidth
        label="Workflow Name"
        value={workflowName}
        onChange={(e) => setWorkflowName(e.target.value)}
        margin="normal"
        required
      />

      <Box sx={{ my: 4 }}>
        <Typography variant="h5" gutterBottom>
          Steps
        </Typography>

        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="steps">
            {(provided) => (
              <div {...provided.droppableProps} ref={provided.innerRef}>
                {steps.map((step, index) => (
                  <Draggable
                    key={index}
                    draggableId={`step-${index}`}
                    index={index}
                  >
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                      >
                        <WorkflowStepForm
                          step={step}
                          index={index}
                          previousSteps={steps.slice(0, index)}
                          onUpdate={handleUpdateStep}
                          onDelete={handleDeleteStep}
                        />
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

        <Button
          variant="outlined"
          color="primary"
          onClick={handleAddStep}
          sx={{ mt: 2 }}
        >
          Add Step
        </Button>
      </Box>

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
        <Button variant="outlined" onClick={() => navigate('/')}>
          Cancel
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={createMutation.isLoading}
        >
          Create Workflow
        </Button>
      </Box>
    </Container>
  );
}

export default CreateWorkflow;