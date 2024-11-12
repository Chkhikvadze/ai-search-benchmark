import { styled } from "styled-components";

const Header = () => {
  return (
    <StyledRoot>
      <StyledCompanyName>
        <StyledLogo src={"DaturaLogo.svg"} alt="logo" />
      </StyledCompanyName>
    </StyledRoot>
  );
};

export default Header;

const StyledRoot = styled.header`
  width: 100%;
  height: 80px;

  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const StyledLogo = styled.img`
  width: 50px;
  height: 50px;
`;

const StyledCompanyName = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 0 20px;
`;
