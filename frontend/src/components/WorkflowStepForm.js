import React from 'react';
import {
  Card,
  CardContent,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Box,
  Typography,
  Collapse,
} from '@mui/material';
import { Delete, DragIndicator } from '@mui/icons-material';

function WorkflowStepForm({ step, index, onUpdate, onDelete }) {
  const handleChange = (field, value) => {
    onUpdate(index, { ...step, [field]: value });
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" alignItems="center">
          <DragIndicator sx={{ mr: 2, cursor: 'move' }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Step {index + 1}
          </Typography>
          <IconButton onClick={() => onDelete(index)} color="error">
            <Delete />
          </IconButton>
        </Box>

        <TextField
          fullWidth
          label="Step Name"
          value={step.step_name}
          onChange={(e) => handleChange('step_name', e.target.value)}
          margin="normal"
        />

        <FormControl fullWidth margin="normal">
          <InputLabel>Action</InputLabel>
          <Select
            value={step.action}
            onChange={(e) => handleChange('action', e.target.value)}
            label="Action"
          >
            <MenuItem value="llm-call">LLM Call</MenuItem>
          </Select>
        </FormControl>

        <TextField
          fullWidth
          label="Prompt"
          value={step.parameters?.prompt || ''}
          onChange={(e) =>
            handleChange('parameters', { ...step.parameters, prompt: e.target.value })
          }
          margin="normal"
          multiline
          rows={2}
        />

        <TextField
          fullWidth
          label="Model"
          value={step.parameters?.model || 'gpt-4-turbo'}
          onChange={(e) =>
            handleChange('parameters', { ...step.parameters, model: e.target.value })
          }
          margin="normal"
        />

        <TextField
          fullWidth
          label="Group (optional)"
          value={step.group || ''}
          onChange={(e) => handleChange('group', e.target.value)}
          margin="normal"
          helperText="Steps with the same group name will execute in parallel"
        />
      </CardContent>
    </Card>
  );
}

export default WorkflowStepForm;
