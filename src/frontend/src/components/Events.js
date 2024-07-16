import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Button, Checkbox, Heading, Link, List, ListItem, Text, VStack, HStack } from "@chakra-ui/react";
import Breadcrumbs from "./Breadcrumbs";

const Events = () => {
  const [events, setEvents] = useState([]);
  const [selectedEvents, setSelectedEvents] = useState([]);

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
    { href: "#/events", label: "Events", isCurrentPage: true },
  ];

  const handleSelectEvent = (eventId) => {
    setSelectedEvents((prev) => {
      if (prev.includes(eventId)) {
        return prev.filter((id) => id !== eventId);
      } else {
        return [...prev, eventId];
      }
    });
  };

  const handleDeleteEvents = () => {
    axios
      .delete("/api/v1/events", { data: { ids: selectedEvents } })
      .then(() => {
        setEvents((prev) => prev.filter((event) => !selectedEvents.includes(event.id)));
        setSelectedEvents([]);
      })
      .catch((error) => console.error("Error deleting events: ", error));
  };

  return (
    <Box p={5} maxW="800px" mx="auto">
      <Breadcrumbs items={breadcrumbItems} />
      <Button colorScheme="red" mb={4} onClick={handleDeleteEvents} isDisabled={selectedEvents.length === 0}>
        Delete Selected
      </Button>
      <List spacing={3}>
        {events.map((event) => (
          <ListItem
            p={3}
            shadow="md"
            borderWidth="1px"
            borderRadius="md"
            mb={3}
            _hover={{ bg: "teal.50" }}
            key={event.id}
          >
            <HStack>
              <Checkbox
                borderColor="gray.400"
                isChecked={selectedEvents.includes(event.id)}
                onChange={() => handleSelectEvent(event.id)}
              />
              <Link as="a" href={`#/events/${event.id}`} _hover={{ textDecoration: "none" }}>
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
              </Link>
            </HStack>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Events;
