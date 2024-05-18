import React from "react";
import Breadcrumbs from "./Breadcrumbs";

const Dashboard = () => {
  const breadcrumbItems = [{ href: "/", label: "Home", isCurrentPage: true }];

  return (
    <div>
      <Breadcrumbs items={breadcrumbItems} />
      <p>All systems operational</p>
    </div>
  );
};

export default Dashboard;
