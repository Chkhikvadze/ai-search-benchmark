import { styled } from "styled-components";
import Typography from "../Typography";

const Header = () => {
  return (
    <StyledRoot>
      <StyledCompanyName>
        <StyledLogo src={"DaturaLogo.svg"} alt="logo" />
        <Typography kind="secondary" semibold size="large">
          Datura Meta
        </Typography>
      </StyledCompanyName>
    </StyledRoot>
  );
};

export default Header;

const StyledRoot = styled.header`
  width: 100%;
  height: 60px;

  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const StyledLogo = styled.img`
  width: 40px;
  height: 40px;
`;

const StyledCompanyName = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 0 20px;
`;
