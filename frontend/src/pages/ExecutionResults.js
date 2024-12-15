import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Container,
  Typography,
  Paper,
  Box,
  List,
  ListItem,
  ListItemText,
  Divider,
  Alert,
} from '@mui/material';
import { workflowApi } from '../api/workflowApi';

function ExecutionResults() {
  const { workflowId } = useParams();

  const { data: results, isLoading, error } = useQuery(
    ['workflowExecution', workflowId],
    () => workflowApi.executeWorkflow(workflowId)
  );

  if (isLoading) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Typography>Executing workflow...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Alert severity="error">
          Error executing workflow: {error.message}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Workflow Results
      </Typography>

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          {results.workflow_name}
        </Typography>

        <List>
          {results.results.map((step, index) => (
            <React.Fragment key={index}>
              {index > 0 && <Divider />}
              <ListItem>
                <ListItemText
                  primary={step.step_name}
                  secondary={
                    <Box>
                      {step.skipped ? (
                        <Typography color="text.secondary">
                          Step was skipped (condition not met)
                        </Typography>
                      ) : step.error ? (
                        <Typography color="error">{step.error}</Typography>
                      ) : (
                        <Typography>{step.result}</Typography>
                      )}
                    </Box>
                  }
                />
              </ListItem>
            </React.Fragment>
          ))}
        </List>
      </Paper>
    </Container>
  );
}

export default ExecutionResults;