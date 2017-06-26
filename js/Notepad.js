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
          const sharedId = item.id.split('-').pop()
          return <LogEntry
            skipAnimation={this.props.skipAnimation}
            isActive={this.props.activeLogEntry === sharedId}
            hover={this.props.hover}
            key={item.id}
            entryId={sharedId}
            bits={item.bits}
            content={item.value} />
        })}
      </div>
    )
  }
}

export default Notepad
