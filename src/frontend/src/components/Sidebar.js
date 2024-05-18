import React from "react";
import { Nav } from "react-bootstrap";
import { NavLink } from "react-router-dom";
import "../styles.css";

const Sidebar = () => {
  return (
    <div className="d-flex flex-column p-3 bg-light" style={{ width: "250px", height: "100vh" }}>
      <Nav className="flex-column">
        <NavLink to="/" activeClassName="nav-link active" class="nav-link">
          Dashboard
        </NavLink>
        <NavLink to="/livefeed" activeClassName="nav-link active" class="nav-link">
          Livefeed
        </NavLink>
        <NavLink to="/events" activeClassName="nav-link active" class="nav-link">
          Events
        </NavLink>
      </Nav>
    </div>
  );
};

export default Sidebar;
