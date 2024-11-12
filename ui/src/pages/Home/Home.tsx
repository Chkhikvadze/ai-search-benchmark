import styled from "styled-components";
import TwitterRelevanceTable from "../../components/Table/TwitterRelevanceTable";
import ProviderPerformanceTable from "../../components/Table/ProviderPerformanceTable";
import Charts from "./components/Charts";

const Home = () => {
  return (
    <StyledRoot>
      <StyledBody>
        <Charts />

        <TwitterRelevanceTable />

        <ProviderPerformanceTable />
      </StyledBody>
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
  gap: 100px;
  flex-direction: column;
`;
