import { styled } from "styled-components";
import Typography from "../Typography";

const Footer = () => {
  return (
    <StyledFooter>
      {/* <Typography kind="primary" bold>
        Datura
      </Typography>
      <p>
        <Typography size="small" kind="secondary">
          Datura provides real-time monitoring for decentralized AI inference on
          the Bittensor network. Track and filter miners and validators by key
          metrics, hotkeys, or IDs, helping you stay informed and manage
          resources efficiently.
        </Typography>
      </p> */}

      <p>
        <Typography size="xs-small" kind="secondary">
          © 2024 Datura. All rights reserved.
        </Typography>
      </p>
    </StyledFooter>
  );
};

export default Footer;
const StyledFooter = styled.footer`
  width: 100%;
  padding: 20px;
  max-width: 600px;

  margin-right: auto;

  margin-top: 150px;

  display: flex;
  flex-direction: column;
  gap: 20px;
`;
