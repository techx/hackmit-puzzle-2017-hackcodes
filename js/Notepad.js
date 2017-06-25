import React from 'react'
import LogEntry from './LogEntry'

class Notepad extends React.Component {
  render () {
    return (
      <div className='notepad display-linebreak'>
        <span className='notepad-heading'> {this.props.title} </span>
        <br />
        <br />
        {this.props.content.map((item) => {
          return <LogEntry
            skipAnimation={this.props.skipAnimation}
            isActive={this.props.activeLogEntry === item.index}
            hover={this.props.hover}
            key={item.index}
            entryId={item.index}
            content={item.value} />
        })}
      </div>
    )
  }
}

export default Notepad
