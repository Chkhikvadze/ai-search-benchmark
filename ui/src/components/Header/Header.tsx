import { styled } from "styled-components";
import Typography from "../Typography";

const Header = () => {
  return (
    <StyledRoot>
      <StyledCompanyName>
        <StyledLogo src={"DaturaLogo.svg"} alt="logo" />
        <Typography>Datura Meta</Typography>
      </StyledCompanyName>
    </StyledRoot>
  );
};

export default Header;

const StyledRoot = styled.header`
  width: 100%;
  height: 60px;
  /* background-color: red; */

  display: flex;
  align-items: center;
  justify-content: space-between;

  /* background-color: ${({ theme }) => theme.body.backgroundColorSecondary}; */
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
