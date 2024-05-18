import React, { useEffect } from "react";
import axios from "axios";
import Breadcrumbs from "./Breadcrumbs";

const Livefeed = () => {
  useEffect(() => {
    // Stop the live feed when the component is unmounted
    const handleUnload = async () => {
      try {
        await axios.post("/api/v1/livefeed/stop");
      } catch (error) {
        console.error("Error stopping live feed", error);
      }
    };

    window.addEventListener("beforeunload", handleUnload);

    return () => {
      window.removeEventListener("beforeunload", handleUnload);
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
