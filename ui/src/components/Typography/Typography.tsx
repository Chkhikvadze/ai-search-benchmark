import styled, { css } from "styled-components";

export interface TypographyProps<T extends React.ElementType> {
  as?: T;
  value?: string;
  children?: React.ReactNode;
  size?: "x-large" | "large" | "medium" | "small" | "xs-small";
  customColor?: string;
  bold?: boolean;
  semibold?: boolean;
  kind?: "primary" | "secondary" | "tertiary" | "quaternary";
}

function Typography<T extends React.ElementType = "span">({
  value,
  children,
  size = "large", // Default size
  customColor,
  bold = false,
  semibold = false,
  kind = "primary",
}: TypographyProps<T> &
  Omit<React.ComponentPropsWithoutRef<T>, keyof TypographyProps<T>>) {
  return (
    <StyledTypography
      style={{ color: customColor }}
      size={size}
      bold={bold}
      semibold={semibold}
      kind={kind}
    >
      {children || value}
    </StyledTypography>
  );
}

export default Typography;

const StyledTypography = styled.span<{
  size: string;
  bold: boolean;
  semibold: boolean;
  kind?: "primary" | "secondary" | "tertiary" | "quaternary";
}>`
  font-style: normal;
  ${(props) =>
    props.size === "large" &&
    css`
      font-size: 18px;
      line-height: 24px;
    `}
  ${(props) =>
    props.size === "x-large" &&
    css`
      font-size: 22px;
      line-height: 26px;
    `}
  ${(props) =>
    props.size === "medium" &&
    css`
      font-size: 16px;
      line-height: 20px;
    `}
  ${(props) =>
    props.size === "small" &&
    css`
      font-size: 14px;
      line-height: 16px;
    `}
  ${(props) =>
    props.size === "xs-small" &&
    css`
      font-size: 12px;
      line-height: 16px;
    `}
  ${(props) =>
    props.bold &&
    css`
      font-weight: bold;
    `}
  ${(props) =>
    props.semibold &&
    css`
      font-weight: 500;
    `}

  ${(props) =>
    props.kind === "primary" &&
    css`
      color: ${props.theme.typography.contentPrimary};
    `}

  ${(props) =>
    props.kind === "secondary" &&
    css`
      color: ${props.theme.typography.contentSecondary};
    `}

  ${(props) =>
    props.kind === "tertiary" &&
    css`
      color: ${props.theme.typography.contentTertiary};
    `}

  ${(props) =>
    props.kind === "quaternary" &&
    css`
      color: ${props.theme.typography.contentQuaternary};
    `}
`;
