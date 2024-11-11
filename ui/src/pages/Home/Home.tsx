import styled from "styled-components";
import Typography from "../../components/Typography";

const Home = () => {
  return (
    <StyledRoot>
      <Typography>Home</Typography>
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
