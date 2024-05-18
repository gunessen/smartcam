import React from "react";
import { Box } from "@chakra-ui/react";
import { Routes, Route } from "react-router-dom";
import Events from "./Events";
import Livefeed from "./Livefeed";
import Dashboard from "./Dashboard";

const MainContent = () => {
  return (
    <Box>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/livefeed" element={<Livefeed />} />
        <Route path="/events" element={<Events />} />
      </Routes>
    </Box>
  );
};

export default MainContent;
