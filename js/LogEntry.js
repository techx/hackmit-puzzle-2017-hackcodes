import React from 'react'

class LogEntry extends React.Component {
  constructor (props) {
    super(props)
    this.onMouseOver = this.onMouseOver.bind(this)
    this.onMouseOut = this.onMouseOut.bind(this)
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
        {this.props.content}
      </div>
    )
  }
}

export default LogEntry
