import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import MenuList from "@mui/material";
import ListItemText from "@mui/material/ListItemText";
import React from "react";
import Grid from "@material-ui/core/Grid";
import {leagues,api_url}  from "./static_vars"
import {
    DataGrid,
    GridToolbarContainer,
    GridToolbarDensitySelector,
    GridToolbarExport,
    GridToolbarFilterButton
} from "@mui/x-data-grid";
import index from "riot-lol/index";

class ChampionMatchHistory extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            rows : [],
            params : props.params,
            version : ""
        }
        this.setState = this.setState.bind(this);
    }

    componentDidMount() {
        fetch(api_url+"competitiveGames/?patch="+this.props.params.patch+"&champion="+this.props.params.champion+"&role="+this.props.params.role+"&leagues="+this.props.params.selectedLeagues+"&format=json").then(response => response.json()).then(data => this.setState(previousState =>({version : previousState.version,rows:data.results, params:previousState.params})));
        fetch("https://ddragon.leagueoflegends.com/api/versions.json").then(response => response.json()).then(data => this.setState(previousState => ({rows:previousState.rows, params:previousState.params, version: data[0]})));
    }
    componentDidUpdate(prevProps, prevState, snapshot) {
        if(!(prevProps.version === this.props.version && prevProps.params.selectedLeagues.toString() === this.props.params.selectedLeagues.toString() && prevProps.params.patch === this.props.params.patch && prevProps.params.champion === this.props.params.champion && prevProps.params.role === this.props.params.role))
            fetch(api_url+"competitiveGames/?patch="+this.props.params.patch+"&champion="+this.props.params.champion+"&role="+this.props.params.role+"&leagues="+this.props.params.selectedLeagues+"&format=json").then(response => response.json()).then(data => this.setState(previousState =>({rows:data.results, params:prevProps.params, version:previousState.version})));
    }

    render() {
        {
        const state = this.state;
        return (
            <div style={{height: 800, width: '25%', gap: "10px"}}>
                <DataGrid rowHeight={60} width={"100%"} /*getRowSpacing={{top:1,bottom:1}}*/ rowSpacingType={"none"}
                    initialState={{
                        sorting: {
                          sortModel: [{ field: 'date', sort: 'desc' }],
                        },
                      }}
                    columns={[
                        {headerName : 'League',field: 'league', width: 150, justifyContent: "center", align: "center", headerAlign: "center"},
                        {headerName : 'By',field: 'team1', width: 40, justifyContent: "center", align: "center", headerAlign: "center", renderCell : (params) => <img src={"https://res.cloudinary.com/xenesis/image/upload/v1/teamsLogo/"+params.value+".png"} width={40} height={40}/>},
                        {field: 'team2', headerName: "Vs", width: 40, justifyContent: "center", align: "center", headerAlign: "center", renderCell : (params) => <img src={"https://res.cloudinary.com/xenesis/image/upload/v1/teamsLogo/"+params.value+".png"} width={40} height={40}/>},
                        {headerName : "Outcome",field: 'outcome', width: 100, justifyContent: "center", align: "center", headerAlign: "center", renderCell : (params) => formatOutcome(params.value)},
                         {headerName : "Performance",field: 'performance', width: 100, justifyContent: "center", align: "center", headerAlign: "center", renderCell : (params) => Math.round(params.value * 100) / 100},
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
}

class ChampionKeystoneSummary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            rows: [],
            params: props.params,
            version: "",
            mythicRows : []
        };
        this.setState = this.setState.bind(this);
    }

    componentDidMount() {
        fetch(api_url + "ChampionsBuildProperties/?patch=" + this.props.params.patch + "&champion=" + this.props.params.champion + "&role=" + this.props.params.role + "&leagues=" + this.props.params.selectedLeagues + "&format=json").then(response => response.json()).then(data => this.setState(previousState => ({
            version: previousState.version,
            rows: data.results[0].keystones,
            params: previousState.params,
            mythicRows : previousState.mythicRows
        })));
        fetch("https://ddragon.leagueoflegends.com/api/versions.json").then(response => response.json()).then(data => this.setState(previousState => ({
            rows: previousState.rows,
            params: previousState.params,
            version: data[0],
            mythicRows : previousState.mythicRows
        })));
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (!(prevProps.version === this.props.version && prevProps.params.selectedLeagues.toString() === this.props.params.selectedLeagues.toString() && prevProps.params.patch === this.props.params.patch && prevProps.params.champion === this.props.params.champion && prevProps.params.role === this.props.params.role))
            fetch(api_url + "ChampionsBuildProperties/?patch=" + this.props.params.patch + "&champion=" + this.props.params.champion + "&role=" + this.props.params.role + "&leagues=" + this.props.params.selectedLeagues + "&format=json").then(response => response.json()).then(data => this.setState(previousState => ({
                rows: data.results[0].keystones,
                params: prevProps.params,
                version: previousState.version,
                mythicRows : data.results[0].first_items
            })));
    }

    render() {
        return (
        <div style={{width: '23%', gap: "10px", position: "sticky", top: "0px", height:800}}>
                <DataGrid rowHeight={60} width={"100%"} /*getRowSpacing={{top:1,bottom:1}}*/ rowSpacingType={"none"}
                    initialState={{
                        sorting: {
                          sortModel: [{ field: 'games', sort: 'desc' }],
                        },
                      }}
                    columns={[
                        {headerName : 'Keystone',field: 'name', width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell : (params) => <img src={"https://res.cloudinary.com/xenesis/image/upload/v1/leagueAssets/"+params.value+".png"} width={40} height={40}/>},
                        {field: 'games', headerName: "Games", width: 80, justifyContent: "center", align: "center", headerAlign: "center"},
                        {headerName : 'Winrate',field: 'winrate', width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell: (params) => params.value.toLocaleString("en", {style: "percent"})},
                        {field: 'performance', headerName: "Perf.", width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell: (params) => Math.round(params.value * 100) / 100},
                        {field: 'relative_performance', headerName: "Relative", width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell: (params) => Math.round(params.value * 100) / 100},

                    ]}
                    rows={this.state.rows}
                    style={{height:"50%"}}
                    hideFooter={true}

                />
                <DataGrid rowHeight={60} width={"100%"} /*getRowSpacing={{top:1,bottom:1}}*/ rowSpacingType={"none"}
                    initialState={{
                        sorting: {
                          sortModel: [{ field: 'games', sort: 'desc' }],
                        },
                      }}
                    columns={[
                        {headerName : '1st item',field: 'name', width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell : (params) => <img src={"https://res.cloudinary.com/xenesis/image/upload/v1/leagueAssets/"+params.value+".png"} width={40} height={40}/>},
                        {field: 'games', headerName: "Games", width: 80, justifyContent: "center", align: "center", headerAlign: "center"},
                        {headerName : 'Winrate',field: 'winrate', width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell: (params) => params.value.toLocaleString("en", {style: "percent"})},
                        {field: 'performance', headerName: "Perf.", width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell: (params) => Math.round(params.value * 100) / 100},
                        {field: 'relative_performance', headerName: "Relative", width: 80, justifyContent: "center", align: "center", headerAlign: "center", renderCell: (params) => Math.round(params.value * 100) / 100},

                    ]}
                    rows={this.state.mythicRows}
                    style={{height:"50%",gap: "10px"}}
                    hideFooter={true}

                />
            </div>)
    }
}
function formatOutcome(result){
    if(result=="0") {
        return "Loss"
    }
    return "Win"
}

function CustomToolbar() {
  return (
    <GridToolbarContainer>
    </GridToolbarContainer>
  );
}

class ChampionMatchups extends React.Component{
    constructor(props) {
        super(props);
        this.props = props
    }

    render() {
        return (
            <Grid container direction={'row'} justifyContent="flex-start" alignItems="flex-end"  wrap='nowrap' style={{wrap:'nowrap', height: '100%', width:"120%"}} >
                <ChampionMatchupsOnRole role={this.props.params.role} patch={this.props.params.patch} leagues = {this.props.params.selectedLeagues} matchupRole = {"TOP_LANE"} champion = {this.props.params.champion} type = {this.props.params.type}/>
                <ChampionMatchupsOnRole role={this.props.params.role} patch={this.props.params.patch} leagues = {this.props.params.selectedLeagues} matchupRole = {"JUNGLE"} champion = {this.props.params.champion} type = {this.props.params.type}/>
                <ChampionMatchupsOnRole role={this.props.params.role} patch={this.props.params.patch} leagues = {this.props.params.selectedLeagues} matchupRole = {"MID_LANE"} champion = {this.props.params.champion} type = {this.props.params.type}/>
                <ChampionMatchupsOnRole role={this.props.params.role} patch={this.props.params.patch} leagues = {this.props.params.selectedLeagues} matchupRole = {"BOT_LANE"} champion = {this.props.params.champion} type = {this.props.params.type}/>
                <ChampionMatchupsOnRole role={this.props.params.role} patch={this.props.params.patch} leagues = {this.props.params.selectedLeagues} matchupRole = {"UTILITY"} champion = {this.props.params.champion} type = {this.props.params.type}/>
            </Grid>
        )
    }
}

class ChampionMatchupsOnRole extends React.Component {
    constructor(props){
        super(props);
        this.props = props;
        this.state = {
            rows: [],
            version : "",
            leagues : props.leagues,
            patch : props.patch
        };
        console.log(this.state.leagues)
    }
    componentDidMount() {
        fetch(api_url + "ChampionsMatchupsProperties/?leagues="+this.state.leagues.toString()+ "&champion=" + this.props.champion +"&role="+this.props.role+"&patch="+this.props.patch+"&format=json&matchup_role="+this.props.matchupRole+"&type="+this.props.type).then(response => response.json()).then(data => this.setState(previousState =>({rows: data.results, version : previousState.version, champions : previousState.version, leagues : previousState.leagues, patch : previousState.patch})));
        fetch("https://ddragon.leagueoflegends.com/api/versions.json").then(response => response.json()).then(data => this.setState(previousState => ({rows:previousState.rows, version:data[0], champions : previousState.version, leagues : previousState.leagues, patch : previousState.patch})));
    }
    componentDidUpdate(prevProps, prevState, snapshot) {
        if (!(prevProps.leagues.toString() === this.props.leagues.toString() && prevProps.patch === this.props.patch && prevProps.champion === this.props.champion && prevProps.role === this.props.role))
            fetch(api_url + "ChampionsMatchupsProperties/?leagues="+this.props.leagues.toString()+ "&champion=" + this.props.champion +"&role="+this.props.role+"&patch="+this.props.patch+"&format=json&matchup_role="+this.props.matchupRole+"&type="+this.props.type).then(response => response.json()).then(data => this.setState(previousState =>({rows: data.results, version : previousState.version, champions : previousState.version, leagues : previousState.leagues, patch : previousState.patch})));
    }

    render()
    {
        const state = this.state;
        return (
            <div style={{height: 1000, gap: "10px", width: '20%'}}>
                <DataGrid rowHeight={60} width={"100%"} /*getRowSpacing={{top:1,bottom:1}}*/ rowSpacingType={"none"}
                    initialState={{
                        sorting: {
                          sortModel: [{ field: 'performance', sort: 'desc' }],
                        },
                      }}
                    columns={[
                        {
                            field: 'champion',
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
                        {headerName : "Performance",field: 'performance', width: 90, renderCell: (params) => formatRating(params), justifyContent: "center", align: "center", headerAlign: "center"},
                        {headerName : "Opp. Perf.",field: 'oppositePerformance', width: 90,renderCell: (params) => formatRating(params), justifyContent: "center", align: "center", headerAlign: "center"},
                    ]}
                    rows={this.state.rows}
                    components={{
                        Toolbar: CustomToolbar,
                    }}
                />
            </div>
        );
    }
}

function formatRating(rating) {
    if(rating.value!="-1000"){
        return Math.round(rating.value * 100) / 100
    }else{
        return ""
    }
}

class ChampionsDetails extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedLeagues: ["LEC", "LCK"],
            patch: "12.10",
            champion: "Aphelios",
            role: "BOT_LANE",
            championNames: [],
            version: ""
        };
        this.setState = this.setState.bind(this);
        fetch("https://ddragon.leagueoflegends.com/api/versions.json").then(response => response.json()).then(data => this.state.version = data[0]).then(fetch("http://ddragon.leagueoflegends.com/cdn/"+this.state.version+"/data/en_US/champion.json").then(response => response.json()).then(data => this.setState(prevState => {
                let name_list = [];
                for(let key in data["data"]){
                    name_list.push(data["data"][key]["name"]);
                }
                let newState = {...prevState};
                newState.championNames = name_list;
                return newState;
            })));
    }

   handleLeagueChange = (event) => {
        this.setState(prevState => {
            let newState = {...prevState};
            newState.selectedLeagues = event.target.value;
            return newState;
        }
        );
        //{ selectedLeagues : event.target.value, patch : this.state.patch, champion : this.state.champion, role : this.state.role}
  };
    handlePatchChange = (event) => {
        this.setState(prevState => {
            let newState = {...prevState};
            newState.patch = event.target.value;
            return newState;
        });
    };
    handleChampionChange = (event) => {
        this.setState(prevState => {
            let newState = {...prevState};
            newState.champion = event.target.value;
            return newState;
        });
    };
    handleRoleChange = (event) => {
        this.setState(prevState => {
            let newState = {...prevState};
            newState.role = event.target.value;
            return newState;
        });
    };

    componentDidUpdate(prevProps, prevState) {
        if(this.state.version !== "" && this.state.championNames.length === 0){
            console.log("Updating champs")
            fetch("http://ddragon.leagueoflegends.com/cdn/"+this.state.version+"/data/en_US/champion.json").then(response => response.json()).then(data => this.setState(prevState => {
                let name_list = [];
                for(let key in data["data"]){
                    name_list.push(data["data"][key]["name"]);
                }
                let newState = {...prevState};
                newState.championNames = name_list;
                return newState;
            }));
        }

    }

    render() {
        return (<div style={{ height: 3000, width:'80%' }}>
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
                            >
                                {league}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <FormControl sx={{m: 1, width: 100, mt: 3}}>
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
                      <MenuItem value={"12.7"}>12.7</MenuItem>
                      <MenuItem value={"12.8"}>12.8</MenuItem>
                      <MenuItem value={"12.9"}>12.9</MenuItem>
                      <MenuItem value={"12.10"}>12.10</MenuItem>
                      <MenuItem value={"12.11"}>12.11</MenuItem>
                      <MenuItem value={"12.12"}>12.12</MenuItem>
                      <MenuItem value={"12.13"}>12.13</MenuItem>
                      <MenuItem value={"12.14"}>12.14</MenuItem>
                      <MenuItem value={"12.15"}>12.15</MenuItem>
                      <MenuItem value={"12.16"}>12.16</MenuItem>
                      <MenuItem value={"12.17"}>12.17</MenuItem>
                      <MenuItem value={"12.18"}>12.18</MenuItem>
                  </Select>
                </FormControl>
                <FormControl sx={{m: 1, width: 200, mt: 3}}>
                  <InputLabel id="champion-select">Champion</InputLabel>
                  <Select
                    labelId="champion-select"
                    id="champion-select"
                    value={this.state.champion}
                    label="Champion"
                    onChange={this.handleChampionChange}
                  >
                      {this.state.championNames.map((champion, index) => (
                          <MenuItem value={champion}>{champion}</MenuItem>
                      ))}
                  </Select>
                </FormControl>
                <FormControl sx={{m: 1, width: 100, mt: 3}}>
                  <InputLabel id="role">Role</InputLabel>
                  <Select
                    labelId="role"
                    id="role"
                    value={this.state.role}
                    label="Champion"
                    onChange={this.handleRoleChange}
                  >
                    <MenuItem value={"TOP_LANE"}>Top</MenuItem>
                    <MenuItem value={"JUNGLE"}>Jungle</MenuItem>
                    <MenuItem value={"MID_LANE"}>Mid</MenuItem>
                    <MenuItem value={"BOT_LANE"}>Adc</MenuItem>
                    <MenuItem value={"UTILITY"}>Support</MenuItem>
                  </Select>
                </FormControl>
            </div>
            <div style={{wrap:'nowrap', marginLeft:'16%'}}>
                <Grid container direction={'row'} justifyContent="flex-start" alignItems="flex-end"  wrap='nowrap' style={{wrap:'nowrap', height: 800, width:5000} } item xs elevation={3}>
                    <ChampionMatchHistory params = {{patch : this.state.patch, selectedLeagues:this.state.selectedLeagues,champion : this.state.champion, role : this.state.role}}/>
                    <ChampionKeystoneSummary params = {{patch : this.state.patch, selectedLeagues:this.state.selectedLeagues,champion : this.state.champion, role : this.state.role}}/>
                </Grid>
                <ChampionMatchups params = {{patch : this.state.patch, selectedLeagues:this.state.selectedLeagues,champion : this.state.champion, role : this.state.role, type : "ennemy"}}/>
                <ChampionMatchups params = {{patch : this.state.patch, selectedLeagues:this.state.selectedLeagues,champion : this.state.champion, role : this.state.role, type : "ally"}}/>
            </div>
        </div>);
            }
}

export default function ChampionsDetailsPage() {
    return (<ChampionsDetails/>)
}