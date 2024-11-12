import styled from "styled-components";
import Header from "../components/Header";

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <StyledRoot>
      <Header />
      <StyledContent>{children}</StyledContent>
    </StyledRoot>
  );
};

export default MainLayout;

const StyledRoot = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: #0a0b0e;
  display: flex;
  flex-direction: column;
`;

const StyledContent = styled.div`
  flex: 1;
  width: 100%;
  height: calc(100% - 80px);
`;
