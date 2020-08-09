import React from 'react';
import axios from 'axios';
import cookie from "react-cookies";

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormGroup from '@material-ui/core/FormGroup';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Avatar from '@material-ui/core/Avatar';
import PersonIcon from '@material-ui/icons/Person';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';

import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import MailIcon from '@material-ui/icons/Mail';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import LockOpenIcon from '@material-ui/icons/LockOpen';
import Icon from '@material-ui/core/Icon';
import Snackbar from '@material-ui/core/Snackbar';
// End Import  ==========================================================================





class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
            login_name:'',
            password:'',
            result: [],
            dialog_visible:false,
            login_failed_snack__visible: false
        
            
    };

 
    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
    this.handleLoginChange = this.handleLoginChange.bind(this);
    this.handlePassChange = this.handlePassChange.bind(this);
     
    this.handleSnackClose = this.handleSnackClose.bind(this);
    this.handleSnackClose = this.handleSnackOpen.bind(this);
     
     
 }
    handleOpen() {
      this.setState({dialog_visible: true}) ;
    };
    
    handleClose () {
      this.setState({ login_name:'',
                       password:'',
                       dialog_visible: false});
    };
    handleSnackOpen() {
      this.setState({login_failed_snack__visible: true}) ;
    };
    
     handleSnackClose () {
     this.setState({login_failed_snack__visible: false}) ;
    };
     handleLogin () {
	     let url='/auth' ;
         const  opts = { login: this.state.login_name,  password: this.state.password        };
    //this.setState({new_category: ''});
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.post(url,opts, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': cookie.load("csrftoken")
      }

      })
      .then((response) => {
        this.setState({
            loaded5: true,
            result5: response.data
        });

      })
      .catch((error) => {

      })
		 
	   
      this.handleClose();
     if (! this.state.loaded5) {
      this.handleSnackOpen()
     } 
    };
    handleLoginChange (event) {
        this.setState({login_name: event.target.value});
	};
    handlePassChange (event ) {
		this.setState({password: event.target.value});
	}

   


 componentDidMount() {
	 	

  


}

    render() {
let  useStyles = makeStyles((theme) => ({
  form: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
      height: '25ch',
    },},	
  root: {
    flexGrow: 1,
  },
  menuButton: {
	
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

let content=
<div>
<p></p>
</div>




return (
   <div>
            <div>
     <Snackbar
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        open={this.login_failed_snack__visible}
        onClose={this.handleSnackClose}
        message="I love snacks"
        //key={vertical + horizontal}
      />
    
       <Dialog onClose={this.handleClose} aria-labelledby="simple-dialog-title" open={this.state.dialog_visible}>
       <DialogTitle id="simple-dialog-title">Авторизация</DialogTitle>
       
      
       <DialogContent>
         <DialogContentText>
            Введите логин и пароль для входа.
          </DialogContentText>
       <TextField  type="text" value={this.state.login_name} onChange={this.handleLoginChange} required id="standard-required" label="Login" defaultValue="Hello World" />
       <TextField
          value={this.state.password} onChange={this.handlePassChange}
          required   id="standard-password-input"
          label="Password"
         
         
          type="password"
          autoComplete="current-password"   />  
      
       
       </DialogContent>
       <DialogActions>
       <Button onClick={this.handleLogin}
        variant="contained"
        color="primary"
      
        startIcon={<LockOpenIcon />}      >
        LOGIN
       </Button>
      
     
         </DialogActions>
        
       </Dialog>
      </div>
       <AppBar position="static">
       <Toolbar>
       <IconButton edge="start"  color="inherit" aria-label="menu"> <MenuIcon /> </IconButton>
       <Typography variant="h6" > News </Typography>
       <Button align="right" onClick={this.handleOpen}  color="inherit"> Login </Button>
       </Toolbar>
       </AppBar>
       {JSON.stringify (this.state)}
    </div>


);


    }
}

export default App;
