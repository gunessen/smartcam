import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { Col, Container, Row } from "react-bootstrap";
import "./App.css";
// import Events from "./components/Events";
import Events from "./components/Events";
import Sidebar from "./components/Sidebar";
import Livefeed from "./components/Livefeed";
import Dashboard from "./components/Dashboard";

const App = () => {
  return (
    <Router>
      <Container fluid>
        <Row>
          <Col md={3}>
            <Sidebar />
          </Col>
          <Col md={9}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/livefeed" element={<Livefeed />} />
              <Route path="/events" element={<Events />} />
            </Routes>
          </Col>
        </Row>
      </Container>
    </Router>
  );
};

export default App;
