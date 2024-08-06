import React from "react";
import { Box } from "@chakra-ui/react";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./Dashboard";
import Livefeed from "./Livefeed";
import Events from "./Events";
import EventDetails from "./EventDetails";
import Settings from "./Settings";

const MainContent = () => {
  return (
    <Box>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/livefeed" element={<Livefeed />} />
        <Route path="/events" element={<Events />} />
        <Route path="/events/:id" element={<EventDetails />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Box>
  );
};

export default MainContent;
