import React from 'react'
import Notepad from './Notepad'
import TimeMachine from './TimeMachine'

class FuturePane extends React.Component {
  getHackmitDate () {
    return 'Sep 2017'
  }

  getTitle() {
    return '~/the-delorean-codes'
  }

  render () {
    return (
      <div className='future'>
        <h1> { this.getHackmitDate() } { this.getTitle() } </h1>

        <TimeMachine />

        <Notepad title='Sent codewords' />

        <br style={{ clear: 'both' }} />
      </div>
    )
  }
}

export default FuturePane
