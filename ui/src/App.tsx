import { ThemeProvider } from "styled-components";
import "./App.css";

import MainLayout from "./Layout/MainLayout";
import Home from "./pages/Home";
import { darkTheme } from "./styles/theme";

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <MainLayout>
        <Home />
      </MainLayout>
    </ThemeProvider>
  );
}

export default App;
