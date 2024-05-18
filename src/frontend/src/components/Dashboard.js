import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Heading, Text, VStack, HStack, Progress, Spinner, Center } from "@chakra-ui/react";
import Breadcrumbs from "./Breadcrumbs";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`/api/v1/stats`)
      .then((response) => {
        setStats(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching event details: ", error);
        setLoading(false);
      });
  }, []);

  console.log(stats);

  const breadcrumbItems = [{ href: "/", label: "Home", isCurrentPage: true }];

  return (
    <Box p={5} maxW="800px" mx="auto">
      <Breadcrumbs items={breadcrumbItems} />
      <Box mt={8} p={5} shadow="md" borderWidth="1px" borderRadius="md">
        <Heading size="lg" color="teal.700" mb={4}>
          System Dashboard
        </Heading>
        {loading ? (
          <Center>
            <Spinner size="xl" />
          </Center>
        ) : (
          <VStack align="start" spacing={4}>
            <Box width="100%">
              <HStack justifyContent="space-between">
                <Text fontWeight="bold">CPU Usage</Text>
                <Text>{stats.cpu_percent}%</Text>
              </HStack>
              <Progress value={stats.cpu_percent} hasStripe colorScheme="teal" size="lg" borderRadius="md" />
            </Box>
            <Box width="100%">
              <HStack justifyContent="space-between">
                <Text fontWeight="bold">RAM Usage</Text>
                {/* <Text>{stats.ram_percent}%</Text> */}
                <Text>
                  {stats.ram_used_mb} / {stats.ram_total_mb} MB ({stats.ram_percent}%)
                </Text>
              </HStack>
              <Progress value={stats.ram_percent} hasStripe colorScheme="teal" size="lg" borderRadius="md" />
            </Box>
            <Box width="100%">
              <HStack justifyContent="space-between">
                <Text fontWeight="bold">Disk Usage</Text>
                <Text>
                  {stats.disk_used_gb} / {stats.disk_total_gb} GB ({stats.disk_percent}%)
                </Text>
              </HStack>
              <Progress value={stats.disk_percent} hasStripe colorScheme="teal" size="lg" borderRadius="md" />
            </Box>
          </VStack>
        )}
      </Box>
    </Box>
  );
};

export default Dashboard;
