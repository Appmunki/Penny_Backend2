var Parse = require('parse');
Parse.initialize(page.data.parse_app_id, page.data.parse_js_api_key);

import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute } from 'react-router';
import DonationList from './components/donations_list.jsx';
import Layout from './components/layout.jsx';
import UserAccount from './components/account.jsx';

import { createHistory, useBasename } from 'history';

import injectTapEventPlugin from 'react-tap-event-plugin';

injectTapEventPlugin();

const history = useBasename(createHistory)({
  basename: '/donation_list'
});
// default behavior
function createElement(Component, props) {
  // make sure you pass all the props in!
  return <Component {...props} screen_name={page.data.currentUserScreenName}/>
}
window.React = React;

ReactDOM.render((
  <Router createElement={createElement} history={history}>
    <Route path="/" component={Layout}>
      <IndexRoute component={DonationList}/>
      <Route path="account" component={UserAccount}/>
    </Route>
  </Router>
), document.getElementById('content'));
