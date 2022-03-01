import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import React from "react";
import Drawer from '@mui/material/Drawer';
import Typography from '@mui/material/Typography';
import Toolbar from "@mui/material/Toolbar";
import { makeStyles } from "@material-ui/core/styles"
import Image from "material-ui-image";
import Box from "@material-ui/core/Box";


export default function Leftbar() {
    return (
        <Drawer variant={"permanent"} open={true} PaperProps={{
            sx: {
                justifyContent: 'top',
                backgroundColor: "#0c1433",
                color: "red",
                width: {sm: `${240}px`}
            }
        }}>
            <Box flexGrow={0.3}><Image src="app_logo.jpg"/></Box>
            <Box flexGrow={1}>
                <Button variant={"text"} color={'text'}>SoloQ Ratings by Role</Button>
                <Button variant={"text"} color={"text"}>SoloQ Champions Details</Button>
                <Button variant={"text"} color={"text"}>SoloQ Players Ratings</Button>
                <Button variant={"text"} color={"text"}>Competitive Champion Ratings by Role</Button>
                <Button variant={"text"} color={"text"}>Competitive Champions Details</Button>
                <Button variant={"text"} color={"text"}>Competitive Players Ratings</Button>
            </Box>
        </Drawer>
    );
};


