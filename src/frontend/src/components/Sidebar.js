import React from "react";
import { Nav } from "react-bootstrap";

const Sidebar = () => {
  return (
    <div className="d-flex flex-column p-3 bg-light" style={{ width: "250px", height: "100vh" }}>
      <Nav className="flex-column">
        <Nav.Link href="/">Dashboard</Nav.Link>
        <Nav.Link href="/livefeed">Livefeed</Nav.Link>
        <Nav.Link href="/events">Events</Nav.Link>
      </Nav>
    </div>
  );
};

export default Sidebar;
