import React from 'react'

class FuturePane extends React.Component {
  getHackmitDate () {
    return 'Sep 2017'
  }

  render () {
    return (
      <div className='future'>
        <h1> { this.getHackmitDate() } </h1>
      </div>
    )
  }
}

export default FuturePane
