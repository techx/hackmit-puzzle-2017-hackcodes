import React from 'react'
import Notepad from './Notepad'

class FuturePane extends React.Component {
  getHackmitDate () {
    return 'Sep 2017'
  }

  render () {
    return (
      <div className='future'>
        <h1> { this.getHackmitDate() } </h1>

        <Notepad />
      </div>
    )
  }
}

export default FuturePane
