import styled from "styled-components";
import TwitterRelevanceTable from "../../components/Table/TwitterRelevanceTable";

const Home = () => {
  return (
    <StyledRoot>
      {/* <Typography>Home</Typography> */}

      <TwitterRelevanceTable />
    </StyledRoot>
  );
};

export default Home;

const StyledRoot = styled.div`
  width: 100%;
  height: 100%;

  padding: 20px;

  /* background-color: red; */
`;
