import React from 'react'

const NUM_LETTERS = 3
const TOTAL_DELAY = 1300
const MAX_DELAY = 100

class LogEntry extends React.Component {
  constructor (props) {
    super(props)
    this.onMouseOver = this.onMouseOver.bind(this)
    this.onMouseOut = this.onMouseOut.bind(this)
    this.state = {
      timer: null,
      count: 0,
      letterIndex: 0,
      content: '',
      fullContent: this.props.content
    }
  }

  componentDidMount () {
    if (this.props.skipAnimation) {
      this.setState({content: this.props.content})
    } else {
      this.animateText()
    }
  }

  componentWillUnmount () {
    clearTimeout(this.state.timer)
  }

  getRandomChar () {
    const alphabet = 'abcdefghijklmnopqrstuvwxyz' +
      'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
      '0123456789'
    const index = Math.floor(alphabet.length * Math.random())
    return alphabet.charAt(index)
  }

  animateText () {
    const fullContent = this.state.fullContent
    if (this.state.content !== fullContent) {
      const count = this.state.count
      const index = this.state.letterIndex
      const prefix = fullContent.substring(0, index)
      const transition = count === NUM_LETTERS
      const nextChar = transition ? '' : this.getRandomChar()
      const delay = TOTAL_DELAY / (fullContent.length * (NUM_LETTERS + 1))
      const timer = setTimeout(
        this.animateText.bind(this),
        Math.min(MAX_DELAY, delay)
      )
      this.setState({
        timer: timer,
        count: transition ? 0 : count + 1,
        letterIndex: transition ? index + 1 : index,
        content: prefix + nextChar
      })
    }
  }

  onMouseOver () {
    this.props.hover(true, this.props.entryId)
  }

  onMouseOut () {
    this.props.hover(false, this.props.entryId)
  }

  render () {
    return (
      <div
        className={this.props.isActive ? 'log-entry active' : 'log-entry'}
        onMouseOver={this.onMouseOver}
        onMouseOut={this.onMouseOut}>
        {this.state.content}
      </div>
    )
  }
}

export default LogEntry
