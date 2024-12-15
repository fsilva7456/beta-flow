import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function NavBar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component={RouterLink} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
          Beta Flow
        </Typography>
        <Button color="inherit" component={RouterLink} to="/create">
          Create Workflow
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;
