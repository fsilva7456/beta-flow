import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  TextField,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import WorkflowStepForm from '../components/WorkflowStepForm';
import { workflowApi } from '../api/workflowApi';

function EditWorkflow() {
  const { workflowId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [error, setError] = useState('');

  // Fetch existing workflow
  const {
    data: workflow,
    isLoading,
    error: fetchError,
  } = useQuery(['workflow', workflowId], () => workflowApi.getWorkflow(workflowId));

  // State for form
  const [workflowName, setWorkflowName] = useState('');
  const [steps, setSteps] = useState([]);

  // Initialize form when data is fetched
  React.useEffect(() => {
    if (workflow) {
      setWorkflowName(workflow.workflow_name);
      setSteps(workflow.steps.map(step => ({
        step_name: step.step_name,
        action: step.action,
        parameters: step.parameters,
        condition: step.condition,
        group: step.group
      })));
    }
  }, [workflow]);

  const updateMutation = useMutation(
    (data) => workflowApi.updateWorkflow(workflowId, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['workflows']);
        navigate('/');
      },
      onError: (error) => {
        setError(error.message);
      },
    }
  );

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

    updateMutation.mutate({
      workflow_name: workflowName,
      steps: steps,
    });
  };

  if (isLoading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (fetchError) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 4 }}>
          Error loading workflow: {fetchError.message}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Edit Workflow
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
          disabled={updateMutation.isLoading}
        >
          Save Changes
        </Button>
      </Box>
    </Container>
  );
}

export default EditWorkflow;