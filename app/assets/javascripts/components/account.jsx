import React from 'react';
import LinkedStateMixin from 'react-addons-linked-state-mixin';

var reqwest = require('../libs/reqwest/reqwest');
var Parse = require('parse').Parse;
var ParseReact = require('parse-react');
import Paper from 'material-ui/lib/paper';
import {FlatButton} from 'material-ui/lib';
import {RaisedButton} from 'material-ui/lib';
import Snackbar from 'material-ui/lib/snackbar';
import {Divider, DatePicker} from 'material-ui/lib';
import {Colors, Spacing, Typography, lightBaseTheme} from 'material-ui/lib/styles';
const FMUI = require('formsy-material-ui');
const { FormsyCheckbox, FormsyDate, FormsyRadio, FormsyRadioGroup, FormsySelect, FormsyText, FormsyTime, FormsyToggle } = FMUI;
var Formsy = require('formsy-react');

const style = {
  raised_button: {
    backgroundColor: '#ff9800'
  },
  raised_button_text: {
    color: Colors.white,
    fontWeight: Typography.fontWeightMedium
  }
};

export default React.createClass({
  mixins: [LinkedStateMixin],

  getInitialState: function () {
    return {
      loading: false,
      snackbaropen: false,
      serverResponse: ''
    }
  },
  computeUserState: function () {
    (new Parse.Query("Tweeters")).equalTo("screen_name", page.data.currentUserScreenName).first({
      success: function (user) {
        var plain_user = user.toPlainObject();

        this.setState({
          user: plain_user,
          card_last4: plain_user.card_last4,
          card_brand: plain_user.card_brand,
          has_account: (plain_user.customer_id && plain_user.account_id),
        });
      }.bind(this)
    });
  },
  componentDidMount: function () {
    if (this.isMounted()) {
      this.computeUserState();
    }
  },
  getUpdateText: function () {
    return this.state.loading ? "Replacing..." : "Replace Card";
  },
  handleSnackbarRequestClose: function () {
    this.setState({snackbaropen: false});
  },
  submit: function (data) {

    this.setState({loading: true});
    reqwest({
      url: '/stripe_user',
      method: 'put',
      data: data,
      success: function (response) {
        this.setState({
          serverResponse: 'Card Replaced',
          snackbaropen: true,
          loading: false
        });
        this.computeUserState();
      }.bind(this)
      , error: function (err) {
        this.setState({
          serverResponse: 'Invalid Debit Card',
          snackbaropen: true,
          loading: false
        });
        this.computeUserState();
      }.bind(this)
    });
  },
  getAccountCard: function () {
    if (!!this.state && !!this.state.card_last4) {
      return (
        <p style={{"lineHeight":"middle","textAlign":"center"}}>
          This account uses: <strong>A {this.state.card_brand}&nbsp;card ending
          in {this.state.card_last4}</strong>
        </p>
      )
    }
  },
  render: function () {
    let styles = {
      form_divider: {
        marginTop: '40px',
        marginBottom: '10px'
      },
      inline_input_left: {
        display: 'inline-block',
        width: '210px',
        marginRight: '20px'
      },
      inline_input_right: {
        display: 'inline-block',
        width: '210px'
      }
    };
    return (
      <div>
        <Paper zDepth={3} className="account_card centered-container">
          {this.getAccountCard()}
        </Paper>
        <Paper zDepth={3} className="account_card centered-container">

          <Formsy.Form
            onSubmit={this.submit}
            validationErrors={this.state.validationErrors}>
            <FormsyText
              fullWidth={true}
              name="debit_card_number"
              validations="isLength:16;isNumeric"
              required
              hintText="XXXX-XXXX-XXXX"
              floatingLabelText="Debit Card Number"/>

            <div style={{"display":"inline-block"}}>
              <div style={{"display":"inline-block"}}>
                <FormsyDate
                  name='exp_date'
                  required
                  floatingLabelText="Expir. Date"
                  />
              </div>
              <div style={{"display":"inline-block"}}>
                <FormsyText
                  style={{"marginLeft":"10px","width":"100px"}}
                  name="cvc"
                  validations="isLength:3;isNumeric"
                  required
                  floatingLabelText="CVC"/>
              </div>
            </div>
            <Divider style={styles.form_divider}/>

            <div style={{"display":"inline-block"}}>
              <FormsyText
                style={styles.inline_input_left}
                name="first_name"
                required
                floatingLabelText="First Name"/>
              <FormsyText
                style={styles.inline_input_right}
                name="last_name"
                required
                floatingLabelText="Last Name"/>
            </div>
            <FormsyDate
              name='dob_date'
              required
              floatingLabelText="Date of Birth"
              />
            <FormsyText
              fullWidth={true}
              name="billing_address_1"
              required
              floatingLabelText="Billing Address 1"/>
            <FormsyText
              fullWidth={true}
              name="billing_address_2"
              floatingLabelText="Billing Address 2"/>

            <div style={{"display":"inline-block"}}>
              <FormsyText
                style={styles.inline_input_left}
                name="city"
                required
                floatingLabelText="City"/>
              <FormsyText
                style={styles.inline_input_right}
                name="state"
                required
                floatingLabelText="State/Province"/>
            </div>
            <FormsyText
              fullWidth={true}
              name="zipcode"
              validations="isLength:5;isNumeric"
              required
              floatingLabelText="Zipcode"/>
            <RaisedButton
              type="submit"
              style={{"marginTop": "20px"}}
              disabled={this.state.loading}
              labelColor={style.raised_button_text.color}
              backgroundColor={style.raised_button.backgroundColor}
              label={this.getUpdateText()}/>
          </Formsy.Form>
        </Paper>
        <Snackbar
          open={this.state.snackbaropen}
          message={this.state.serverResponse}
          onRequestClose={this.handleSnackbarRequestClose}
          autoHideDuration={4000}
          />
      </div>
    )
  }
});
