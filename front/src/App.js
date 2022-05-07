import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';
import Header from "./header";
import Leftbar from "./leftbar";
import theme from "./theme";
import React from "react";
import { ThemeProvider } from '@mui/material/styles';
import ChampionsTierlistPage from "./champions_tierlists"
import Drawer from "@mui/material/Drawer";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import ChampionsDetailsPage from "./champion_details"


function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function App() {
    const [value, setValue] = React.useState(0);
    const handleChange = (event, newValue) => {
    setValue(newValue);
    };
    let competitiveRatingsState = {
        selectedLeagues: ["LEC","LCK"],
        patch: "12.6",
        rows: [],
        version : ""
    };

    return (
        <div className="App">
            <ThemeProvider theme={theme}>
                <Header/>
                <Leftbar/>
                <Tabs value={value} aria-label="basic tabs example" onChange={handleChange} style={{wrap:'nowrap', marginLeft:'16%', height: '100%'}}>
                  <Tab label="Champions Ratings" {...a11yProps(0)} />
                  <Tab label="Champion Details" {...a11yProps(1)} />
                  <Tab label="Item Three" {...a11yProps(2)} />
                </Tabs>
                <TabPanel value={value} index={0}>
                    <ChampionsTierlistPage state={competitiveRatingsState}/>
                  </TabPanel>
                  <TabPanel value={value} index={1}>
                    <ChampionsDetailsPage/>
                  </TabPanel>
                  <TabPanel value={value} index={2}>
                    Item Three
                  </TabPanel>
            </ThemeProvider>
        </div>
    );
}

export default App;
