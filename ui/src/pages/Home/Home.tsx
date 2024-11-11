import styled from "styled-components";
import TwitterRelevanceTable from "../../components/Table/TwitterRelevanceTable";
import ProviderPerformanceTable from "../../components/Table/ProviderPerformanceTalble";

const Home = () => {
  return (
    <StyledRoot>
      {/* <Typography>Home</Typography> */}

      <TwitterRelevanceTable />

      <ProviderPerformanceTable />
    </StyledRoot>
  );
};

export default Home;

const StyledRoot = styled.div`
  width: 100%;
  height: 100%;

  padding: 20px;
`;
