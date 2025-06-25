import React, { ReactNode } from "react";

interface TableProps {
  children: ReactNode;
}

interface HeadProps {
  children: ReactNode;
}

interface HeadCellProps {
  children: ReactNode;
}

interface BodyProps {
  children: ReactNode;
}

interface RowProps {
  children: ReactNode;
  hoverable?: boolean;
}

interface CellProps {
  children: ReactNode;
  className?: string;
}

export const Table: React.FC<TableProps> = ({ children }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm text-left text-gray-500">
        {children}
      </table>
    </div>
  );
};

export const Head: React.FC<HeadProps> = ({ children }) => {
  return (
    <thead className="text-xs text-gray-700 uppercase bg-gray-50">
      <tr>{children}</tr>
    </thead>
  );
};

export const HeadCell: React.FC<HeadCellProps> = ({ children }) => {
  return (
    <th scope="col" className="px-6 py-3">
      {children}
    </th>
  );
};

export const Body: React.FC<BodyProps> = ({ children }) => {
  return <tbody className="divide-y divide-gray-100">{children}</tbody>;
};

export const Row: React.FC<RowProps> = ({ children, hoverable = false }) => {
  return (
    <tr className={`${hoverable ? "hover:bg-gray-50" : ""} bg-white border-b`}>
      {children}
    </tr>
  );
};

export const Cell: React.FC<CellProps> = ({ children, className }) => {
  return <td className={`px-6 py-4 ${className}`}>{children}</td>;
};
