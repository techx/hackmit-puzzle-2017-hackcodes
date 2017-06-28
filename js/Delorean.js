import React from 'react'
import axios from 'axios'
import FormData from 'form-data'
import FuturePane from './FuturePane'
import PresentPane from './PresentPane'

class Delorean extends React.Component {
  constructor (props) {
    super(props)
    this.hover = this.hover.bind(this)
    this.send = this.send.bind(this)
    this.clear = this.clear.bind(this)

    const codewords = this.retrieve('deloreanCodesCodewords') || []
    const messages = this.retrieve('deloreanCodesMessages') || []
    if (codewords === null) this.store('deloreanCodesCodewords', [])
    if (messages === null) this.store('deloreanCodesMessages', [])
    this.state = {
      codewords: codewords,
      messages: messages,
      activeLogEntry: null,
      examples: {codewords: [], messages: []}
    }

    this.loadExamples()
  }

  loadExamples () {
    axios
      .get('/api/examples', {
        params: {username: USERNAME}
      })
      .then((response) => {
        const codewords = response.data.map((example, i) => {
          return {
            id: 'ex-codeword-' + i,
            value: example.codeword,
            bits: false
          }
        })
        const messages = response.data.map((example, i) => {
          return {
            id: 'ex-message--' + i,
            value: example.message,
            bits: example.message_bits
          }
        })
        this.setState({
          examples: {codewords: codewords, messages: messages}
        })
      })
  }

  store (key, value) {
    localStorage.setItem(key, JSON.stringify(value))
  }

  retrieve (key) {
    const raw = localStorage.getItem(key)
    return raw === null ? raw : JSON.parse(raw)
  }

  getCurrentDate () {
    const date = new Date()
    const month = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ][date.getMonth()]
    const year = date.getYear() + 1900
    return month + ' ' + year
  }

  getCodewords () {
    return this.state.codewords.concat(
      this.state.examples.codewords
    )
  }

  getMessages () {
    return this.state.messages.concat(
      this.state.examples.messages
    )
  }

  hover (isBeginHover, entryId) {
    this.setState({
      activeLogEntry: isBeginHover ? entryId : null
    })
  }

  send (codeword) {
    const data = new FormData()
    data.append('username', USERNAME)
    data.append('codeword', codeword)
    axios
      .post('/api/decode', data)
      .then((response) => {
        this.handleSendResponse(codeword, response)
      })
  }

  handleSendResponse (codeword, response) {
    const data = response.data
    const time = +new Date()
    this.setState({
      codewords: [{
        id: 'codeword-' + time,
        value: codeword,
        bits: false
      }].concat(this.state.codewords)
    })
    this.setState({
      messages: [{
        id: 'message-' + time,
        value: data.well_formed ? data.message : false,
        bits: data.message_bits
      }].concat(this.state.messages)
    })
    this.store('deloreanCodesCodewords', this.state.codewords)
    this.store('deloreanCodesMessages', this.state.messages)

    if (data.answer) {
      alert('nice job :) puzzle answer: ' + data.answer)
    }
  }

  clear () {
    this.setState({codewords: []})
    this.setState({messages: []})
    this.store('deloreanCodesCodewords', [])
    this.store('deloreanCodesMessages', [])
  }

  render () {
    return (
      <div className='container'>
        <FuturePane
          currentDate={this.getCurrentDate()}
          notepadContent={this.getCodewords()}
          activeLogEntry={this.state.activeLogEntry}
          hover={this.hover}
          send={this.send}
          clear={this.clear}
          />

        <PresentPane
          currentDate={this.getCurrentDate()}
          notepadContent={this.getMessages()}
          activeLogEntry={this.state.activeLogEntry}
          hover={this.hover} />

        <br style={{clear: 'both'}} />
      </div>
    )
  }
}

export default Delorean
