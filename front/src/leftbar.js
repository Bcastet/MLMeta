import Button from "@mui/material/Button";
import React from "react";
import Drawer from '@mui/material/Drawer';
import Image from "material-ui-image";
import Box from "@material-ui/core/Box";


export default function Leftbar() {
    return (
        <Drawer variant={"permanent"} open={true} PaperProps={{
            sx: {
                justifyContent: 'top',
                backgroundColor: "#0c1433",
                color: "red",
                width: '12.5%',
                variant:"persistent"
            }
        }}>
            <Box flexGrow={0.3}><Image src="app_logo.jpg"/></Box>
            <Box flexGrow={1}>
                <Button variant={"text"} color={'text'}>Competitive Metagame</Button>
                <Button variant={"text"} color={"text"}>Competitive Players</Button>
                <Button variant={"text"} color={"text"}>Competitive Teams</Button>
                <Button variant={"text"} color={"text"}>SoloQ Metagame</Button>
                <Button variant={"text"} color={"text"}>SoloQ Players</Button>
            </Box>
        </Drawer>
    );
};


