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
      activeLogEntry: null
    }
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
    return array.map((value, i) => {
      return {value: value, index: array.length - (i + 1)}
    })
  }

  getCodewords () {
    const codewords = this.state.codewords.concat([
      'codeword 3',
      'codeword 2',
      'codeword 1'
    ])
    return this.reverseIndex(codewords)
  }

  getMessages () {
    const messages = this.state.messages.concat([
      'message 3',
      'message 2',
      'message 1'
    ])
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
    const message = data.well_formed ? data.message : false
    this.setState({
      codewords: [codeword].concat(this.state.codewords)
    })
    this.setState({
      messages: [message].concat(this.state.messages)
    })
    this.store('deloreanCodesCodewords', this.state.codewords)
    this.store('deloreanCodesMessages', this.state.messages)
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
