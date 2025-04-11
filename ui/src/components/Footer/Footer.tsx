import { styled } from "styled-components";
import Typography from "../Typography";
import { FaGithub, FaDiscord } from "react-icons/fa"; // Import GitHub and Discord icons
import { discordUrl, githubUrl } from "../../constants";

const Footer = () => {
  return (
    <StyledFooter>
      {/* <Typography kind="primary" bold>
        Desearch
      </Typography>
      <p>
        <Typography size="small" kind="secondary">
          Desearch provides real-time monitoring for decentralized AI inference on
          the Bittensor network. Track and filter miners and validators by key
          metrics, hotkeys, or IDs, helping you stay informed and manage
          resources efficiently.
        </Typography>
      </p> */}

      <p>
        <Typography size="xs-small" kind="secondary">
          © 2024 Desearch. All rights reserved.
        </Typography>
      </p>

      <IconLinks>
        <a href={githubUrl} target="_blank" rel="noopener noreferrer">
          <FaGithub size={24} />
        </a>
        <a href={discordUrl} target="_blank" rel="noopener noreferrer">
          <FaDiscord size={24} />
        </a>
      </IconLinks>
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

const IconLinks = styled.div`
  display: flex;
  gap: 10px;

  a {
    opacity: 0.5;
    color: ${({ theme }) => theme.body.iconColor};
    transition: opacity 0.2s;

    &:hover {
      opacity: 1;
    }
  }
`;
