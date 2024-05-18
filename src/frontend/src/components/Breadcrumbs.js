import React from "react";
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink } from "@chakra-ui/react";
import { ChevronRightIcon } from "@chakra-ui/icons";

const Breadcrumbs = ({ items }) => {
  return (
    <Breadcrumb spacing="8px" mb={5} separator={<ChevronRightIcon color="gray.500" />}>
      {items.map((item, index) => (
        <BreadcrumbItem key={index} isCurrentPage={item.isCurrentPage}>
          <BreadcrumbLink href={item.href}>{item.label}</BreadcrumbLink>
        </BreadcrumbItem>
      ))}
    </Breadcrumb>
  );
};

export default Breadcrumbs;
