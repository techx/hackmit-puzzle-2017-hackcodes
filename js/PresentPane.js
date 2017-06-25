import React from 'react'
import Notepad from './Notepad'

class PresentPane extends React.Component {
  render () {
    return (
      <div className='present'>
        <h1> { this.props.currentDate } </h1>

        <Notepad title='Received messages' />
      </div>
    )
  }
}

export default PresentPane