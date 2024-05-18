import React, { useEffect } from "react";
import axios from "axios";
import Breadcrumbs from "./Breadcrumbs";

const Livefeed = () => {
  useEffect(() => {
    // Use cleanup function to stop the live feed
    const handleStopLivefeed = async () => {
      try {
        await axios.post("/api/v1/livefeed/stop");
      } catch (error) {
        console.error("Error stopping live feed", error);
      }
    };

    // Stop the live feed when the component is unmounted
    return () => {
      handleStopLivefeed();
    };
  }, []);

  const breadcrumbItems = [
    { href: "/", label: "Home" },
    { href: "/livefeed", label: "Livefeed", isCurrentPage: true },
  ];

  return (
    <div>
      <Breadcrumbs items={breadcrumbItems} />
      <img src="/api/v1/livefeed" alt="Livefeed" />
    </div>
  );
};

export default Livefeed;
