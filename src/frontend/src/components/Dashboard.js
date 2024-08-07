import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Heading,
  Text,
  VStack,
  HStack,
  IconButton,
  Progress,
  Spinner,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverArrow,
  PopoverCloseButton,
  PopoverHeader,
  PopoverBody,
  Center,
} from "@chakra-ui/react";
import { InfoIcon } from "@chakra-ui/icons";

import Breadcrumbs from "./Breadcrumbs";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = () => {
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
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);

    return () => clearInterval(interval);
  }, []);

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
              <HStack justifyContent="space-between" mb={1}>
                <HStack>
                  <Text fontWeight="bold">CPU Usage</Text>
                  <Popover>
                    <PopoverTrigger>
                      <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                    </PopoverTrigger>
                    <PopoverContent>
                      <PopoverArrow />
                      <PopoverCloseButton />
                      <PopoverHeader>CPU Usage</PopoverHeader>
                      <PopoverBody>
                        The percentage of CPU usage is important to monitor to ensure that the system is not overloaded.
                      </PopoverBody>
                    </PopoverContent>
                  </Popover>
                </HStack>
                <Text>{stats.cpu_percent}%</Text>
              </HStack>
              <Progress value={stats.cpu_percent} hasStripe colorScheme="teal" size="lg" borderRadius="md" />
            </Box>
            <Box width="100%">
              <HStack justifyContent="space-between" mb={1}>
                <HStack>
                  <Text fontWeight="bold">RAM Usage</Text>
                  <Popover>
                    <PopoverTrigger>
                      <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                    </PopoverTrigger>
                    <PopoverContent>
                      <PopoverArrow />
                      <PopoverCloseButton />
                      <PopoverHeader>RAM Usage</PopoverHeader>
                      <PopoverBody>
                        RAM usage is the percentage of memory that is being used by the system. It is important to
                        monitor this to ensure that the system is not running out of memory.
                      </PopoverBody>
                    </PopoverContent>
                  </Popover>
                </HStack>
                <Text>
                  {stats.ram_used_mb} / {stats.ram_total_mb} MB ({stats.ram_percent}%)
                </Text>
              </HStack>
              <Progress value={stats.ram_percent} hasStripe colorScheme="teal" size="lg" borderRadius="md" />
            </Box>
            <Box width="100%">
              <HStack justifyContent="space-between" mb={1}>
                <HStack>
                  <Text fontWeight="bold">Disk Usage</Text>
                  <Popover>
                    <PopoverTrigger>
                      <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                    </PopoverTrigger>
                    <PopoverContent>
                      <PopoverArrow />
                      <PopoverCloseButton />
                      <PopoverHeader>Disk Usage</PopoverHeader>
                      <PopoverBody>
                        Disk usage is the percentage of disk space that is being used by the system. It is important to
                        monitor this to ensure that the system is not running out of disk space.
                      </PopoverBody>
                    </PopoverContent>
                  </Popover>
                </HStack>
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
