import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';
import Header from "./header";
import Leftbar from "./leftbar";
import theme from "./theme";
import React from "react";
import { ThemeProvider } from '@mui/material/styles';
import Drawer from "@mui/material/Drawer";


function App() {
    return (

        <div className="App">
            <ThemeProvider theme={theme}>
                <Header/>
                <Leftbar/>
            </ThemeProvider>
        </div>
    );
}

export default App;
