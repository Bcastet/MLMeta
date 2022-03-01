import React from 'react';
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import {makeStyles} from "@material-ui/core/styles";
import Box from '@material-ui/core/Box';


export default function Header() {
    return (
        <AppBar position="relative">
            <Toolbar>
                <Box display='flex' flexGrow={1}>{}</Box>
                <Button color="inherit" sx={{ alignItems: "flex-end" }}>Contact</Button>
                <Button color="inherit" sx={{ alignItems: "flex-end" }}>About</Button>
            </Toolbar>
        </AppBar>
    );
}