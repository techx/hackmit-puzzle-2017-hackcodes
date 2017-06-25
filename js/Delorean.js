import React from 'react'
import FuturePane from './FuturePane'
import PresentPane from './PresentPane'

class Delorean extends React.Component {
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
      <div className='container'>
        <FuturePane currentDate={this.getCurrentDate()} />

        <PresentPane currentDate={this.getCurrentDate()} />

        <br style={{clear: 'both'}} />
      </div>
    )
  }
}

export default Delorean
