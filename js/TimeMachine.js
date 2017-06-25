import React from 'react'
import axios from 'axios'
import FormData from 'form-data'

class TimeMachine extends React.Component {
  constructor () {
    super()
    this.send = this.send.bind(this)
  }

  getTargetMessage () {
    return 'send me across'
  }

  send () {
    const codeword = document.getElementById('codeword').value
    const data = new FormData()
    data.append('codeword', codeword)
    axios
      .post('/api/decode', data)
      .then(this.handleSendResponse)
      .catch((error) => { console.log(error) })
  }

  handleSendResponse (response) {
    const data = response.data
    console.log(data.message)
  }

  clear () {
    console.log('clear')
  }

  render () {
    return (
      <div className='time-machine'>
        <p>
          You've just had the best idea of your life, but it's the month
          after HackMIT. Desperate, you've broken into the MIT time
          machine lab! You need to figure out how to transmit the
          following message back to { this.props.currentDate }:
        </p>

        <pre> { this.getTargetMessage() } </pre>

        <p>
          There's one problem: time machines shuffle up data really
          <i> really </i> badly, so the researchers at this lab have
          to do some clever stuff to get info through to the other side...
        </p>

        <textarea id='codeword' />

        <a id='send-button' className='button' onClick={this.send}>
          Send message
        </a>

        <a id='clear-button' className='button' onClick={this.clear}>
          Clear logs
        </a>
      </div>
    )
  }
}

export default TimeMachine
