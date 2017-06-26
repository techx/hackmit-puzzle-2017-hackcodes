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
    const username = window.location.href.split('/').pop()
    axios
      .get('/api/examples', {
        params: {username: username}
      })
      .then((response) => {
        const codewords = response.data.map((example) => {
          return {value: example.codeword, bits: false}
        })
        const messages = response.data.map((example) => {
          return {value: example.message, bits: example.message_bits}
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

  reverseIndex (array) {
    return array.map((item, i) => {
      item.index = array.length - (i + 1)
      return item
    })
  }

  getCodewords () {
    const codewords = this.state.codewords.concat(
      this.state.examples.codewords
    )
    return this.reverseIndex(codewords)
  }

  getMessages () {
    const messages = this.state.messages.concat(
      this.state.examples.messages
    )
    return this.reverseIndex(messages)
  }

  hover (isBeginHover, entryId) {
    this.setState({
      activeLogEntry: isBeginHover ? entryId : null
    })
  }

  send (codeword) {
    const username = window.location.href.split('/').pop()
    const data = new FormData()
    data.append('username', username)
    data.append('codeword', codeword)
    axios
      .post('/api/decode', data)
      .then((response) => {
        this.handleSendResponse(codeword, response)
      })
  }

  handleSendResponse (codeword, response) {
    const data = response.data
    this.setState({
      codewords: [{
        value: codeword,
        bits: false
      }].concat(this.state.codewords)
    })
    this.setState({
      messages: [{
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
