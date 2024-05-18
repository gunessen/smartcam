import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { Box, Heading, Text, VStack, HStack } from "@chakra-ui/react";
import Breadcrumbs from "./Breadcrumbs";

const EventDetails = () => {
  const { id } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    axios
      .get(`/api/v1/events/${id}`)
      .then((response) => {
        setEvent(response.data);
      })
      .catch((error) => console.error("Error fetching event details: ", error));
  }, [id]);

  const breadcrumbItems = [
    { href: "/", label: "Home" },
    { href: "#/events", label: "Events" },
    { href: `#/events/${id}`, label: "Event Details", isCurrentPage: true },
  ];

  if (!event) {
    return <Text>Loading...</Text>;
  }

  return (
    <Box p={5} maxW="800px" mx="auto">
      <Breadcrumbs items={breadcrumbItems} />
      <Box mt={8} p={5} shadow="md" borderWidth="1px" borderRadius="md">
        <VStack align="start" spacing={4}>
          <Heading size="lg" color="teal.700">
            Event Details
          </Heading>
          <HStack>
            <Text fontWeight="bold">Detected:</Text>
            <Text>{event.objects}</Text>
          </HStack>
          <HStack>
            <Text fontWeight="bold">Video path:</Text>
            <Text>{event.video_path}</Text>
          </HStack>
          <HStack>
            <Text fontWeight="bold">Event time:</Text>
            <Text>{event.event_time}</Text>
          </HStack>
          <HStack>
            <Text fontWeight="bold">Video length:</Text>
            <Text>{event.video_length}</Text>
          </HStack>
          <Box mt={4} width="100%">
            <video controls width="100%">
              <source src={`/api/v1/events/${id}/video`} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </Box>
        </VStack>
      </Box>
    </Box>
  );
};

export default EventDetails;
