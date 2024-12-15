import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, CssBaseline, Container, Typography } from '@mui/material';
import theme from './theme';

import NavBar from './components/NavBar';
import Home from './pages/Home';
import CreateWorkflow from './pages/CreateWorkflow';
import EditWorkflow from './pages/EditWorkflow';
import ExecutionResults from './pages/ExecutionResults';
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: 1,
        onError: (error) => {
          console.error('Query error:', error);
        }
      }
    }
  });

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Router>
            <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
              <NavBar />
              <Container component="main" sx={{ flex: 1, py: 3 }}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/create" element={<CreateWorkflow />} />
                  <Route path="/edit/:workflowId" element={<EditWorkflow />} />
                  <Route path="/results/:workflowId" element={<ExecutionResults />} />
                  <Route path="*" element={<Typography>Page not found</Typography>} />
                </Routes>
              </Container>
            </div>
          </Router>
        </ThemeProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;