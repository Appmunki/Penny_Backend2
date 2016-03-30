import React from 'react';
import { History, Link } from 'react-router'
import { LinkContainer } from 'react-router-bootstrap';

var util = require('util');
var ReactBootstrap = require('react-bootstrap');
var NavDropdown = ReactBootstrap.NavDropdown;
var MenuItem = ReactBootstrap.MenuItem;


export default React.createClass({
  mixins: [History],

  render: function () {

    return (
      <div>
        {this.renderHeader()}
        <div className="container penny-background">
          {this.props.children}
        </div>
      </div>
    )
  },
  renderHeader: function () {
    return (
      <nav id="penny-navbar"
           className="navbar navbar-default navbar-fixed-top ">
        <div className="container">
          <Link className="navbar-brand penny-secondary-color" to="/">Penny</Link>
          <ul className="nav navbar-nav navbar-right">
            {this.renderNavbarDropdown()}
          </ul>
        </div>
      </nav>
    );
  },
  navigateToAccountPage(){
    this.history.pushState(null, '/account', null)
  },
  navigateToAboutPage(){
    this.history.pushState(null, '/about', null)
  },
  renderNavbarDropdown(){
    return (
      <NavDropdown eventKey={4} title={this.props.screen_name} id="nav-dropdown">
        <LinkContainer to='/account'>
          <MenuItem eventKey="4.1" >Account</MenuItem>
        </LinkContainer>
        <MenuItem divider/>
        <MenuItem eventKey="4.3" href="/logout">Logout</MenuItem>
      </NavDropdown>
    );
  }
});