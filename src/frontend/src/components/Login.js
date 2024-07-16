import React, { useState, useContext } from "react";
import { Box, Button, Flex, FormControl, FormLabel, Input, VStack, useToast } from "@chakra-ui/react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

const Login = ({ history }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { setAuthStatus } = useContext(AuthContext);
  const toast = useToast();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post("/api/v1/login", { username, password });
      if (response.data) {
        setAuthStatus(true);
        navigate("/");
      }
    } catch (error) {
      console.log(error);
      toast({
        title: "Login failed",
        description: error.response.data.message,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Flex minHeight="100vh" width="full" align="center" justifyContent="center">
      <Box p={4} maxW="sm" borderWidth="2px" borderRadius="lg" overflow="hidden" borderColor="gray.300">
        <form onSubmit={handleLogin}>
          <VStack spacing={4}>
            <FormControl id="username" isRequired>
              <FormLabel>Username</FormLabel>
              <Input
                type="text"
                borderColor="gray.300"
                borderWidth="2px"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </FormControl>
            <FormControl id="password" isRequired>
              <FormLabel>Password</FormLabel>
              <Input
                type="password"
                borderColor="gray.300"
                borderWidth="2px"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormControl>
            <Button type="submit" colorScheme="teal">
              Login
            </Button>
          </VStack>
        </form>
      </Box>
    </Flex>
  );
};

export default Login;
