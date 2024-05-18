import { HashRouter as Router } from "react-router-dom";

import { Box, Grid } from "@chakra-ui/react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";

const App = () => {
  return (
    <Router>
      <Box p={4}>
        <Grid templateColumns="200px 1fr" gap={6}>
          <Sidebar />
          <MainContent />
        </Grid>
      </Box>
    </Router>
  );
};

export default App;
