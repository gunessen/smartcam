import React from "react";
import { NavLink } from "react-router-dom";
import { VStack, Button } from "@chakra-ui/react";

const Sidebar = () => {
  return (
    <VStack as="nav" bg="gray.100" p={4} borderRadius="md" spacing={4} align="stretch">
      <Button
        as={NavLink}
        to="/"
        colorScheme="teal"
        variant="ghost"
        _activeLink={{ fontWeight: "bold", color: "teal.600", bg: "teal.200" }}
      >
        Dashboard
      </Button>
      <Button
        as={NavLink}
        to="/livefeed"
        colorScheme="teal"
        variant="ghost"
        _activeLink={{ fontWeight: "bold", color: "teal.600", bg: "teal.200" }}
      >
        Livefeed
      </Button>
      <Button
        as={NavLink}
        to="/events"
        colorScheme="teal"
        variant="ghost"
        _activeLink={{ fontWeight: "bold", color: "teal.600", bg: "teal.200" }}
      >
        Events
      </Button>
    </VStack>
  );
};

export default Sidebar;
