import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { VStack, Button } from "@chakra-ui/react";
import { AuthContext } from "../contexts/AuthContext";

const Sidebar = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

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
      <Button
        as={NavLink}
        to="/settings"
        colorScheme="teal"
        variant="ghost"
        _activeLink={{ fontWeight: "bold", color: "teal.600", bg: "teal.200" }}
      >
        Settings
      </Button>
      <Button onClick={handleLogout} colorScheme="teal" variant="ghost">
        Logout
      </Button>
    </VStack>
  );
};

export default Sidebar;
