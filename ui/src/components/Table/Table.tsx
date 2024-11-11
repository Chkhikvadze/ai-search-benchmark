import React from "react";
import { useTable, useSortBy } from "react-table";
import styled from "styled-components";

import { FaSortUp, FaSortDown } from "react-icons/fa";

interface TableProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  columns: any;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: any;
}

const Table: React.FC<TableProps> = ({ columns, data }) => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const sortByEnabled = columns.some((column: any) => column.sort);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data }, ...(sortByEnabled ? [useSortBy] : []));

  return (
    <TableContainer>
      <StyledTable {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
              {headerGroup.headers.map((column: any) => (
                <StyledTh
                  {...column.getHeaderProps(
                    column.sort ? column.getSortByToggleProps() : undefined
                  )}
                  style={{
                    width: column.width,
                    minWidth: column.minWidth,
                  }}
                >
                  <StyledHeaderRow>
                    {column.render("Header")}
                    {column.sort && (
                      <StyledSymbol>
                        <StyledIcon
                          as={FaSortUp}
                          active={column.isSorted && !column.isSortedDesc}
                        />
                        <StyledIcon
                          as={FaSortDown}
                          active={column.isSorted && column.isSortedDesc}
                        />
                      </StyledSymbol>
                    )}
                  </StyledHeaderRow>
                </StyledTh>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <StyledTd {...cell.getCellProps()}>
                    {cell.render("Cell")}
                  </StyledTd>
                ))}
              </tr>
            );
          })}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default Table;

const TableContainer = styled.div`
  overflow-x: auto;
`;

const StyledTable = styled.table`
  border-radius: 10px;

  width: 100%;

  font-size: 14px;
`;

const StyledTh = styled.th`
  border-bottom: 1px solid #2a2b2e;
  /* background: ${({ theme }) => theme.body.detailCardBackgroundColor}; */
  color: ${({ theme }) => theme.body.textColorSecondary};
`;

const StyledTd = styled.td`
  text-align: center;
  padding: 10px;

  color: ${({ theme }) => theme.body.textColorSecondary};
  border-bottom: 1px solid #26272b81;
`;

const StyledHeaderRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  padding: 10px;
`;

const StyledSymbol = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const StyledIcon = styled.div<{ active: boolean }>`
  opacity: ${({ active }) => (active ? 1 : 0.4)};
`;
