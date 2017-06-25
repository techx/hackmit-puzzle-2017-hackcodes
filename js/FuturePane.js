import React from 'react'
import Notepad from './Notepad'
import TimeMachine from './TimeMachine'

class FuturePane extends React.Component {
  getHackmitDate () {
    return 'Sep 2017'
  }

  render () {
    return (
      <div className='future'>
        <h1> { this.getHackmitDate() } </h1>

        <TimeMachine />

        <Notepad title='Sent codewords' />

        <br style={{ clear: 'both' }} />
      </div>
    )
  }
}

export default FuturePane
