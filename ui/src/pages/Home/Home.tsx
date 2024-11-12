import styled from "styled-components";
import TwitterRelevanceTable from "../../components/Table/TwitterRelevanceTable";
import ProviderPerformanceTable from "../../components/Table/ProviderPerformanceTable";
import Charts from "./components/Charts";
import Footer from "../../components/Footer";

const Home = () => {
  return (
    <StyledRoot>
      <StyledBody>
        <StyledTitle>Meta Leaderboard</StyledTitle>

        <Charts />

        <TwitterRelevanceTable />

        <ProviderPerformanceTable />
      </StyledBody>

      <Footer />
    </StyledRoot>
  );
};

export default Home;

const StyledRoot = styled.div`
  width: 100%;
  height: 100%;

  padding: 20px;

  overflow-y: auto;

  display: flex;
  flex-direction: column;
  align-items: center;
`;

const StyledBody = styled.div`
  width: 100%;
  max-width: 1400px;

  display: flex;
  gap: 80px;
  flex-direction: column;
  align-items: center;
`;

const StyledTitle = styled.h1`
  background: linear-gradient(90deg, #989bff, #4e54fc 50%, #4e54fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
`;
