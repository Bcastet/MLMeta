import React from 'react';
import FormControl from '@mui/material/FormControl';
import {
  DataGrid,
  GridToolbarContainer,
  GridToolbarFilterButton,
  GridToolbarExport,
  GridToolbarDensitySelector,
} from '@mui/x-data-grid';
import Grid from '@material-ui/core/Grid'
import Select from '@mui/material/Select';
import {leagues, api_url} from "./static_vars"
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';


const MenuProps = {
  PaperProps: {
    style: {
      width: 250,
    },
  },
};

class ChampionsTierlist extends React.Component {
    constructor(props){
        super(props);
        this.props = props;
        this.state = {
            rows: [],
            version : "",
            leagues : props.leagues,
            patch : props.patch
        };
        this.setState(props.state);
    }
    componentDidMount() {
        //var leaguesString =
        fetch(api_url + "ratings/?leagues="+this.state.leagues.toString()+"&role="+this.props.role+"&patch="+this.props.patch+"&format=json").then(response => response.json()).then(data => this.setState(previousState =>({rows: data.results, version : previousState.version, champions : previousState.version, leagues : previousState.leagues, patch : previousState.patch})));
        fetch("https://ddragon.leagueoflegends.com/api/versions.json").then(response => response.json()).then(data => this.setState(previousState => ({rows:previousState.rows, version:data[0], champions : previousState.version, leagues : previousState.leagues, patch : previousState.patch})));
    }
    componentDidUpdate(prevProps, prevState) {
        console.log()
        if(!(prevProps.version === this.props.version && prevProps.leagues.toString() === this.props.leagues.toString() && prevProps.patch === this.props.patch)){
            fetch("http://127.0.0.1:8000/ratings/?leagues="+this.props.leagues.toString()+"&role="+this.props.role+"&patch="+this.props.patch+"&format=json").then(response => response.json()).then(data => this.setState(previousState =>({rows: data.results, version : previousState.version, champions : previousState.version, leagues : previousState.leagues, patch : previousState.patch})));
            console.log("Updated")
        }
    }


    render()
    {
        const state = this.state;
        return (
            <div style={{height: '100%', width: '21.5%', gap: "10px"}}>
                <DataGrid rowHeight={60} width={"100%"} /*getRowSpacing={{top:1,bottom:1}}*/ rowSpacingType={"none"}
                    initialState={{
                        sorting: {
                          sortModel: [{ field: 'rel_rate', sort: 'desc' }],
                        },
                      }}
                    columns={[
                        {
                            field: 'name',
                            headerName: "Champion",
                            hideable: false,
                            renderCell: (params) => <img src={"https://ddragon.leagueoflegends.com/cdn/"+state.version+"/img/champion/"+params.value+".png"} width="60" height="60"/>,
                            width: 90,
                            height: 40,
                            align: "center",
                            headerAlign: "center"
                        },
                        {headerName : 'Games',field: 'games', width: 60, justifyContent: "center", align: "center", headerAlign: "center"},
                        {field: 'winrate', headerName: "WR", width: 60, justifyContent: "center", renderCell: (params) => params.value.toLocaleString("en", {style: "percent"}), align: "center", headerAlign: "center"},
                        {headerName : "Rating",field: 'rel_rate', width: 90, justifyContent: "center", renderCell: (params) => Math.round(params.value * 100) / 100, align: "center", headerAlign: "center"},
                    ]}
                    rows={state.rows}
                    components={{
                        Toolbar: CustomToolbar,
                    }}
                />
            </div>
        );
    }
}

function CustomToolbar() {
  return (
    <GridToolbarContainer>
      <GridToolbarFilterButton />
      <GridToolbarDensitySelector />
      <GridToolbarExport />
    </GridToolbarContainer>
  );
}


class LeagueSelector extends React.Component {
    constructor(props) {
        super(props);
        console.log(props.state)
        this.state = {
            selectedLeagues: ["LEC", "LCK"],
            patch: "12.6",
            rows: [],
            version: ""
        };
        //props.setState(props.state);
        this.setState = this.setState.bind(this);
        this.setState(props.state);
    }

   handleLeagueChange = (event) => {
        this.setState(
          { selectedLeagues : event.target.value, patch : this.state.patch}
        );
        this.props.state = this.state;
  };
    handlePatchChange = (event) => {
        this.setState(
          { selectedLeagues : this.state.selectedLeagues, patch : event.target.value}
        );
        this.props.state = this.state;
    }
    render() {
        return (
            <div style={{ height: 3000, width:'80%' }}>
                <div>
            <FormControl sx={{m: 1, width: 300, mt: 3}}>
                <InputLabel id="league-select">League</InputLabel>
                <Select
                    multiple
                    displayEmpty
                    value={this.state.selectedLeagues}
                    onChange={this.handleLeagueChange}
                    label={"Leagues"}
                    labelId="league-select"
                    id="league-select"
                >
                    <MenuItem disabled value="">
                    </MenuItem>
                    {leagues.map((league) => (
                        <MenuItem
                            key={league}
                            value={league}
                            //style={getStyles(name, personName, theme)}
                        >
                            {league}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
                    <FormControl sx={{m: 1, width: 300, mt: 3}}>
                      <InputLabel id="patch-select">Patch</InputLabel>
                      <Select
                        labelId="patch-select"
                        id="patch-select"
                        value={this.state.patch}
                        label="Patch"
                        onChange={this.handlePatchChange}
                      >
                        <MenuItem value={"12.4"}>12.4</MenuItem>
                        <MenuItem value={"12.5"}>12.5</MenuItem>
                        <MenuItem value={"12.6"}>12.6</MenuItem>
                      </Select>
                    </FormControl>
        </div>
                <Grid container direction={'row'} justifyContent="flex-start" alignItems="flex-end"  wrap='nowrap' style={{wrap:'nowrap', marginLeft:'16%', height: '100%'}} >
                    <ChampionsTierlist role={"TOP_LANE"} patch={this.state.patch} leagues = {this.state.selectedLeagues}/>
                    <ChampionsTierlist role={"JUNGLE"} patch={this.state.patch} leagues = {this.state.selectedLeagues}/>
                    <ChampionsTierlist role={"MID_LANE"} patch={this.state.patch} leagues = {this.state.selectedLeagues}/>
                    <ChampionsTierlist role={"BOT_LANE"} patch={this.state.patch} leagues = {this.state.selectedLeagues}/>
                    <ChampionsTierlist role={"UTILITY"} patch={this.state.patch} leagues = {this.state.selectedLeagues}/>
                </Grid>
        </div>);
    }
}

export default function ChampionsTierlistPage(state) {
    return (<LeagueSelector state={state}/>)
}