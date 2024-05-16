import React, { useEffect, useState } from "react";
import axios from "axios";

const Events = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    axios
      .get("/api/v1/events")
      .then((response) => {
        console.log(response.data);
        setEvents(response.data);
      })
      .catch((error) => console.error("Error fetching events: ", error));
  }, []);

  return (
    <div>
      <h1>Events</h1>
      <ul>
        {events.map((event) => (
          <li key={event.id}>
            {event.video_path}: {event.objects}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Events;
