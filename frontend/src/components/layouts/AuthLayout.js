import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Box, Container, Paper, Typography } from '@mui/material';
import { AuthContext } from '../../context/AuthContext';

const AuthLayout = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);

  // If authenticated, redirect to dashboard
  if (isAuthenticated && !loading) {
    return <Navigate to="/dashboard" />;
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        backgroundColor: 'background.default',
      }}
    >
      <Container component="main" maxWidth="xs" sx={{ mt: 8 }}>
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h4" sx={{ mb: 2 }}>
            ISP Customer Portal
          </Typography>
          <Outlet />
        </Paper>
      </Container>
      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: 'background.paper',
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} ISP Technician Routing System
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default AuthLayout;
