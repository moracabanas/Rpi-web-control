import logo from './logo.svg';
import './App.css';
import socketIOClient from "socket.io-client";
import React, { useState, useEffect } from "react";
import { styled } from '@material-ui/core/styles';
import { Button, Grid, Paper, TextField, makeStyles, InputLabel} from '@material-ui/core';

const ENDPOINT = "http://ec2-34-242-65-242.eu-west-1.compute.amazonaws.com:5000";


const useStyles = makeStyles((theme) => ({
  input: {
    color: "#FFF",
  },
}));

var socket

function App() {
  
  useEffect(()=> {

  var sid = -1
   socket = socketIOClient(ENDPOINT);
  socket.on("message", (data) => {

      data = JSON.parse(data.replace(/'/g, '"'))
      // console.log(data)


      if(data.state === 'room-non-existent'){
        alert('Room not found!')
        // setIsDisabled("false")
      }else if (data.state === 'joined-room'){
        alert('Connected to Room: ' + data.room)
        sid = data.sid
        setIsDisabled("true")
      }else if (data.state === 'leaved-room'){
        console.log(data)
        if(data.sid === sid){
          setIsDisabled('')
          sid = -1
        }
      }else if (data.state === 'close-room'){

          setIsDisabled('')   
          sid = -1   
          alert('this room has been closed!')
      }else if (data.num === "0"){
        setBlack()
        setFirstB('#0004ff')
      }else if (data.num === "1"){
        setBlack()
        setSecondB('#ff9400')
      }else if (data.num === "2"){
        setBlack()
        setThirdB('#ff00b4')
      }else if (data.num === "3"){
        setBlack()
        setFourthB('#ff0000')
      }

    })
    return () => {
      socket.emit('leave', { 'room': code })
    }
  }, []) 
 


  const classes = useStyles();
 

  const [code, setCode] = useState('');
  const [isDisabled, setIsDisabled] = useState('');

  const [firstB,  setFirstB] = useState('#000157');   // #0004ff
  const [secondB, setSecondB] = useState('#6b3e00');  // #ff9400
  const [thirdB,  setThirdB] = useState('#3d002b');   // #ff00b4
  const [fourthB, setFourthB] = useState('#3d0200');  // #ff0000

 

  function setBlack () {
    setFirstB('#000157')
    setSecondB('#6b3e00')
    setThirdB('#3d002b')
    setFourthB('#3d0200')
  }

  function firstButton() {
    console.log('First Button Message')
    socket.emit("messages", { room: code, message: '0' } ); 
  }

  function secondButton() {
    console.log('Second Button Message')
    socket.emit("messages", { room: code, message: '1' } ); 
  }

  function thirdButton() {
    console.log('Third Button Message')
    socket.emit("messages", { room: code, message: '2' } ); 
  }

  function fourthButton() {
    console.log('Fourth Button Message')
    socket.emit("messages", { room: code, message: '3' } ); 
  }

  function sendButton() {
    console.log('Send Button Message')
    if(isDisabled === ''){
      socket.emit("join", { room: code } ); 
      // socket.emit('join', {room: ""})
      alert('conectando ...', code.toString())
    }else{
      socket.emit('leave', { "room": code })
    }
    
  }
  

  return (
    <div className="App">
      <header className="App-header">
     
      <Grid  container direction="row" spacing={1} >

        <Grid item xs={12}>
          <h2>SocialStation.it</h2>
        </Grid>

        <Grid item xs={12}>
         <TextField disabled={isDisabled} variant="outlined" value={code} onChange={e => setCode(e.target.value)} inputProps={{ className: classes.input }} placeholder='Code' ></TextField>
          <Button onClick={sendButton} variant="outlined" color="primary" style={{width: "60px", height: "55px", color:isDisabled === ''? "green" : "red", borderColor: isDisabled === ''? "green" : "red"}}>Send</Button>
        </Grid>

        <Grid item xs={6}>
          <Button onClick={firstButton} variant="outlined" color="primary" style={{width: "150px", height: "150px", color: "blue", borderColor: "blue"}}>
            Primary
          </Button>
        </Grid>

        <Grid item xs={6}>
          <Button onClick={secondButton} variant="outlined" color="primary" style={{width: "150px", height: "150px", color: "orange", borderColor: "orange"}}>
            Second
          </Button>
        </Grid>

        <Grid item xs={6}>
          <Button onClick={thirdButton} variant="outlined" color="primary" style={{width: "150px", height: "150px", color: "magenta", borderColor: "magenta"}}>
            Third
          </Button>
        </Grid>
        
        <Grid item xs={6}>
          <Button onClick={fourthButton} variant="outlined" style={{width: "150px", height: "150px", color: "red", borderColor: "red"}}>
            Fourth
          </Button>
        </Grid>

{/* states */}

        <Grid item xs={3} container direction="column" justify="center" alignItems="center">
          <InputLabel style={{width: "40px", height: "40px", color: "blue", borderColor: "blue", backgroundColor: firstB }}>
          </InputLabel>
        </Grid>

        <Grid item xs={3} container direction="column" justify="center" alignItems="center">
          <InputLabel style={{width: "40px", height: "40px", color: "orange", borderColor: "orange", backgroundColor: secondB }}>
          </InputLabel>
        </Grid>

        <Grid item xs={3} container direction="column" justify="center" alignItems="center">
          <InputLabel style={{width: "40px", height: "40px", color: "magenta", borderColor: "magenta", backgroundColor: thirdB }}>
          </InputLabel>
        </Grid>

        <Grid item xs={3} container direction="column" justify="center" alignItems="center">
          <InputLabel style={{width: "40px", height: "40px", color: "red", borderColor: "blue", backgroundColor: fourthB}}>
          </InputLabel>
        </Grid> 

      </Grid>
       

      </header>



    </div>
  );
}

export default App;
