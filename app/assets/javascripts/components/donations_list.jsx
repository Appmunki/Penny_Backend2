import React from 'react';
import { Link }  from 'react-router';
import Layout from './layout.jsx';
var Parse = require('parse').Parse;
var ParseReact = require('parse-react');
import Card from 'material-ui/lib/card/card';
import { Table } from 'react-bootstrap';
import Paper from 'material-ui/lib/paper';


const colWidths = {
  numberColWidth: {
    width: '10%',
    paddingRight: '0'
  },
  userColWidth: {
    width: '40%'
  },
  userDataColWidth: {
    width: '40%',
    textAlign: 'center'
  },
  amountColWidth: {
    width: '20%'
  },
  statusColWidth: {
    width: '30%'
  }
};

export default React.createClass({
  mixins: [ParseReact.Mixin], // Enable query subscriptions

  observe: function () {
    // Subscribe to all Comment objects, ordered by creation date
    // The results will be available at this.data.comments
    return {
      sender_donations: (new Parse.Query("Donation")).equalTo("sender", this.props.screen_name),
      receiver_donations: (new Parse.Query("Donation")).equalTo("receiver", this.props.screen_name)
    };
  },
  renderDonationTable: function (tableName, donationRows) {
    return (
      <div className="col-md-6">
        <Paper className="donation-table" zDepth={3}>
          <Table >
            <thead>
            <tr>
              <th colSpan="4" style={{textAlign: 'center'}}>
                <h2 className="text-success">{tableName} Transactions</h2>
              </th>
            </tr>
            <tr>
              <th >#</th>
              <th >User</th>
              <th >Amount</th>
              <th >Status</th>
            </tr>
            </thead>
            <tbody>
            {donationRows}
            </tbody>
          </Table>
        </Paper>
      </div>
    );
  },
  render: function () {
    var receiverRows = this.renderReceiverDonationTable(this.data.receiver_donations);
    var senderRows = this.renderSenderDonationTable(this.data.sender_donations);

    return (
      <div>
        <div className="row">
          {this.renderDonationTable('Received', receiverRows)}
          {this.renderDonationTable('Sent', senderRows)}
        </div>
      </div>
    )
  },
  renderReceiverDonationTable: function (donations) {
    return donations.map(function (c, i) {
      return (
        <tr>
          <td>{i}</td>
          <td>
            <a href={'https://twitter.com/'+c.sender}>@{c.sender}</a>
          </td>
          <td >${c.amount}</td>
          <td>
            <p className={(c.status==='pending') ? 'text-danger' : 'text-success'}>{c.status}</p>
          </td>
        </tr>
      );
    })
  },
  renderSenderDonationTable: function (donations) {
    return donations.map(function (c, i) {
      return (
        <tr>
          <td>{i}</td>
          <td>
            <a href={'https://twitter.com/'+c.receiver}>@{c.receiver}</a>
          </td>
          <td>
            ${c.amount}
          </td>
          <td>
            <p className={(c.status==='pending') ? 'text-danger' : 'text-success'}>{c.status}</p>
          </td>
        </tr>
      );
    });
  }
})
;
