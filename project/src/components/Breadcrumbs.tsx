import React from "react";
import { Home } from "lucide-react";
import { Link } from "react-router-dom";

interface BreadcrumbsProps {
  currentPage: string;
  parentPage?: string;
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  currentPage,
  parentPage = "dashboard",
}) => {
  const capitalize = (str: string) =>
    str.charAt(0).toUpperCase() + str.slice(1);

  const isSame = currentPage.toLowerCase() === parentPage.toLowerCase();

  return (
    <nav
      aria-label="breadcrumb"
      className="flex items-center space-x-1 text-gray-400 text-sm"
    >
      <Link to={`/${parentPage}`} className="flex items-center hover:text-white">
        <Home className="h-4 w-4 text-cyan-400" />
        {isSame && <span className="ml-1 text-white">{capitalize(currentPage)}</span>}
        {!isSame && <span className="ml-1">{capitalize(parentPage)}</span>}
      </Link>
      {!isSame && (
        <>
          <span className="text-gray-500 select-none"> / </span>
          <span className="text-white">{capitalize(currentPage)}</span>
        </>
      )}
    </nav>
  );
};
