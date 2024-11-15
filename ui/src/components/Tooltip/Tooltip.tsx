import React, { useState } from "react";
import styled from "styled-components";
import { FaInfoCircle } from "react-icons/fa"; // Example icon from react-icons

const Tooltip: React.FC<{ text: string }> = ({ text }) => {
  const [visible, setVisible] = useState(false);

  return (
    <TooltipContainer
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      <FaInfoCircle size={14} />
      <TooltipText visible={visible}>{text}</TooltipText>
    </TooltipContainer>
  );
};

export default Tooltip;

const TooltipContainer = styled.div`
  position: relative;
  display: inline-block;
  cursor: pointer;
`;

const TooltipText = styled.div<{ visible: boolean }>`
  visibility: ${({ visible }) => (visible ? "visible" : "hidden")};
  width: 200px;
  background-color: ${({ theme }) => theme.body.textColorPrimary};
  color: ${({ theme }) => theme.body.textColorTertiary};
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 200%; /* Position above the icon */
  left: 50%;
  margin-left: -100px; /* Adjusted for arrow */
  opacity: ${({ visible }) => (visible ? 1 : 0)};
  transition: opacity 0.3s;
  font-size: 14px;

  &::after {
    content: "";
    position: absolute;
    top: 100%; /* Position at the bottom of the tooltip */
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;

    border-color: ${({ theme }) => theme.body.textColorPrimary} transparent
      transparent transparent;
  }
`;
