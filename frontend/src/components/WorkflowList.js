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
import { PlayArrow } from '@mui/icons-material';

function WorkflowList({ workflows, onExecute }) {
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
                  variant="contained"
                  color="primary"
                  startIcon={<PlayArrow />}
                  onClick={() => onExecute(workflow.id)}
                  sx={{ mr: 1 }}
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
