import React from 'react'
import Notepad from './Notepad'

class PresentPane extends React.Component {
  getCurrentDate () {
    const date = new Date()
    const month = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ][date.getMonth()]
    const year = date.getYear() + 1900
    return month + ' ' + year
  }

  render () {
    return (
      <div className='present'>
        <h1> { this.getCurrentDate() } </h1>

        <Notepad />
      </div>
    )
  }
}

export default PresentPane
