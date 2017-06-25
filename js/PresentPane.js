import React from 'react'
import Notepad from './Notepad'

class PresentPane extends React.Component {
  render () {
    return (
      <div className='present'>
        <h1> {this.props.currentDate} </h1>

        <Notepad
          title='Received messages'
          content={this.props.notepadContent}
          activeLogEntry={this.props.activeLogEntry}
          hover={this.props.hover} />
      </div>
    )
  }
}

export default PresentPane
