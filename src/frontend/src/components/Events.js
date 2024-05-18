import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles.css";

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

  return (
    <div className="container mt-5">
      <h1>Events</h1>
      <ul className="list-group">
        {events.map((event) => (
          <a href="#{event.id}" className="list-group-item">
            <div className="row">
              <h4 class="list-group-item-heading">Detected: {formatObjects(event.objects)}</h4>
              <p class="list-group-item-text">
                <strong>Video path</strong>: {event.video_path}
              </p>
              <p class="list-group-item-text">
                <strong>Event time</strong>: {event.event_time}
              </p>
              <p class="list-group-item-text">
                <strong>Video length</strong>: {event.video_length}
              </p>
            </div>
          </a>
        ))}
      </ul>
    </div>
  );
};

export default Events;
