import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Heading, Link, List, ListItem, Text, VStack, HStack } from "@chakra-ui/react";
import Breadcrumbs from "./Breadcrumbs";

const Events = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    axios
      .get("/api/v1/events")
      .then((response) => {
        setEvents(response.data);
      })
      .catch((error) => console.error("Error fetching events: ", error));
  }, []);

  const formatObjects = (objects) => {
    // Convert the objects to an array if it's not already
    if (Array.isArray(objects)) {
      return objects.join(", ");
    } else if (typeof objects === "object") {
      return Object.values(objects).join(", ");
    } else if (typeof objects === "string") {
      return objects.replace(/[\{\}']/g, "").replace(/,/g, ", ");
    }
    return objects.toString();
  };

  const breadcrumbItems = [
    { href: "/", label: "Home" },
    { href: "/events", label: "Events", isCurrentPage: true },
  ];

  return (
    <Box p={5} maxW="800px" mx="auto">
      <Breadcrumbs items={breadcrumbItems} />
      <List spacing={3}>
        {events.map((event) => (
          <Link href={`#${event.id}`} _hover={{ textDecoration: "none" }} key={event.id}>
            <ListItem p={3} shadow="md" borderWidth="1px" borderRadius="md" mb={3} _hover={{ bg: "teal.50" }}>
              <VStack align="start" spacing={2}>
                <Heading size="md" color="teal.700">
                  Detected: {formatObjects(event.objects)}
                </Heading>
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
              </VStack>
            </ListItem>
          </Link>
        ))}
      </List>
    </Box>
  );
};

export default Events;
