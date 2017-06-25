import React from 'react'
import LogEntry from './LogEntry'

class Notepad extends React.Component {
  render () {
    return (
      <div className='notepad display-linebreak'>
        <span className='notepad-heading'> {this.props.title} </span>
        <br />
        <br />
        {this.props.content.map((item, key) => {
          return <LogEntry
            isActive={this.props.activeLogEntry === key}
            hover={this.props.hover}
            key={key}
            entryId={key}
            content={item} />
        })}
      </div>
    )
  }
}

export default Notepad
