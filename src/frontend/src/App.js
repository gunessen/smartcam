import React from "react";
import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Box, Grid } from "@chakra-ui/react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import Login from "./components/Login";
import { AuthProvider, AuthContext } from "./contexts/AuthContext";

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/*"
            element={
              <AuthContext.Consumer>
                {({ isAuthenticated }) =>
                  isAuthenticated ? (
                    <Box p={4}>
                      <Grid templateColumns="200px 1fr" gap={6}>
                        <Sidebar />
                        <MainContent />
                      </Grid>
                    </Box>
                  ) : (
                    <Navigate to="/login" />
                  )
                }
              </AuthContext.Consumer>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
