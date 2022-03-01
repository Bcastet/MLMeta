import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      light: '#757ce8',
      main: '#0c1433',
      dark: '#0d1e50',
      contrastText: '#fff',
    },
    secondary: {
      light: '#ff7961',
      main: '#ba000d',
      dark: '#ba000d',
      contrastText: '#000',
    },
    background:{
      main: '#2c2c2c',
    },
    text:{
      main: '#ffffff',
    }
  },
});

export default theme