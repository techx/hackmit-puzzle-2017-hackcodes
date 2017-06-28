import React from 'react'
import axios from 'axios'

class TimeMachine extends React.Component {
  constructor (props) {
    super(props)
    this.send = this.send.bind(this)
    this.onKeyDown = this.onKeyDown.bind(this)
    this.onChange = this.onChange.bind(this)
    this.state = {challenge: '', codeword: ''}
    this.loadChallenge()
  }

  loadChallenge () {
    axios
      .get('/api/challenge', {
        params: {username: USERNAME}
      })
      .then((response) => {
        this.setState({challenge: response.data.message})
      })
  }

  send () {
    this.props.send(this.state.codeword)

    // feedback to user that case doesn't matter
    this.setState({codeword: this.state.codeword.toLowerCase()})
  }

  onKeyDown (e) {
    if (e.key === 'Enter') {
      e.preventDefault()
      this.send()
      return false
    }
  }

  onChange (e) {
    this.setState({codeword: e.target.value})
  }

  render () {
    return (
      <div className='time-machine'>
        <p>
          You've just had the best idea of your life, but it's the month
          after HackMIT. Desperate, you've broken into the MIT time
          machine lab! You need to figure out how to transmit the
          following message back to {this.props.currentDate}:
        </p>

        <pre>{this.state.challenge}</pre>

        <p>
          There's one problem: time machines shuffle up data really
          <i> really </i> badly, so the researchers at this lab have
          to do some clever stuff to get info through to the other side...
        </p>

        <textarea
          onKeyDown={this.onKeyDown}
          onChange={this.onChange}
          value={this.state.codeword} />

        <a id='send-button' className='button' onClick={this.send}>
          Send message
        </a>

        <a id='clear-button' className='button' onClick={this.props.clear}>
          Clear logs
        </a>
      </div>
    )
  }
}

export default TimeMachine
