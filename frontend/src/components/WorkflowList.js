import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  Button,
  Paper,
  Typography,
  Box,
} from '@mui/material';
import { PlayArrow, Edit } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

function WorkflowList({ workflows, onExecute }) {
  const navigate = useNavigate();

  if (!workflows.length) {
    return (
      <Paper sx={{ p: 2, textAlign: 'center' }}>
        <Typography>No workflows found. Create your first workflow!</Typography>
      </Paper>
    );
  }

  return (
    <List>
      {workflows.map((workflow) => (
        <Paper key={workflow.id} sx={{ mb: 2 }}>
          <ListItem
            secondaryAction={
              <Box>
                <Button
                  variant="outlined"
                  color="primary"
                  startIcon={<Edit />}
                  onClick={() => navigate(`/edit/${workflow.id}`)}
                  sx={{ mr: 1 }}
                >
                  Edit
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<PlayArrow />}
                  onClick={() => onExecute(workflow.id)}
                >
                  Execute
                </Button>
              </Box>
            }
          >
            <ListItemText
              primary={workflow.workflow_name}
              secondary={`Created: ${new Date(workflow.created_at).toLocaleDateString()}`}
            />
          </ListItem>
        </Paper>
      ))}
    </List>
  );
}

export default WorkflowList;