import React from 'react';
import ReactDOM from 'react-dom';
import { History, Link } from 'react-router'

import Paper from 'material-ui/lib/paper';
var ReactBootstrap = require('react-bootstrap');
var NavDropdown = ReactBootstrap.NavDropdown;
var MenuItem = ReactBootstrap.MenuItem;
import {Colors, Spacing, Typography, lightBaseTheme} from 'material-ui/lib/styles';
import RaisedButton from 'material-ui/lib/raised-button';
import TypeWriter from 'react-typewriter';

const style = {
  height: 200,
  width: 360,
  margin: '20px auto 0',
  padding: '30',
  display: 'block'
};

window.React = React;

const typewritertext = ['Hey @Ryan, here\'s $200 for rent', 'Thanks for the concert last night $20 @Jen'];

var LoginComponent = React.createClass({
  getInitialState: function () {
    return {
      currentTypeWriterIndex: 0
    }
  },
  getTypeWriterText: function () {

    return typewritertext[this.state.currentTypeWriterIndex];
  },
  resetTypeWriter: function () {
    var resetHeaderFunc = function () {
      this.state.currentTypeWriterIndex++;
      if (this.state.currentTypeWriterIndex >= typewritertext.length) this.setState({currentTypeWriterIndex: 0});

      var headerTypeWriter = this.refs.headerTypeWriter;
      headerTypeWriter.setState({visibleChars: 0});
      this.forceUpdate()
    }.bind(this);
    setTimeout(resetHeaderFunc, 5000);
  },
  render: function () {
    let styles = {
      main_logo: {
        fontWeight: Typography.fontWeightMedium,
        margin: 'auto auto',
        textAlign: 'center',
        display: 'block'
      },
      login_text: {
        color: '#FF8C01',
        fontWeight: Typography.fontWeightMedium,
        margin: 'auto auto',
        textAlign: 'center',
        display: 'block'
      },
      login_button: {
        backgroundColor: Colors.white,
        labelColor: '#55acee',
        margin: '0 auto'
      }
    };
    return (
      <div className="landing-page">
        <div >
          <div className="container">
            <div className="row">
              <div className="col-xs-3">
                <h2 className="white-text" style={styles.main_logo}>Penny</h2>
              </div>
            </div>
          </div>
          <section className="mainsection">
            <div className="align-center">
              <h1 className="white-text"><TypeWriter ref="headerTypeWriter"
                                                     onTypingEnd={this.resetTypeWriter}
                                                     typing={1}>{this.getTypeWriterText()}
              </TypeWriter><span> #giveapenny</span></h1>
              <h4 className="white-text">Send money Instantly and Socially.</h4>

              <div className="button-area">
                <div style={{"textAlign":"center"}}>
                  <RaisedButton style={{"width": "200px"}} linkButton={true} href="/login/signin_with_twitter"
                                backgroundColor={styles.login_button.backgroundColor}
                                labelColor={styles.login_button.labelColor}
                                label="Twitter Login" labelPosition="after">
                    <i className="zmdi zmdi-twitter zmdi-hc-lg login-button-logo"></i>
                  </RaisedButton>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    );
  }
});

ReactDOM.render(
  <LoginComponent />,
  document.getElementById('content'));
