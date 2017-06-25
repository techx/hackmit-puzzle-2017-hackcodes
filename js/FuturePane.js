import React from 'react'
import Notepad from './Notepad'
import TimeMachine from './TimeMachine'

class FuturePane extends React.Component {
  getHackmitDate () {
    return 'Oct 2017'
  }

  getTitle () {
    return '~/the-delorean-codes'
  }

  render () {
    return (
      <div className='future'>
        <h1 className='normal'>
          {this.getHackmitDate()} {this.getTitle()}
        </h1>
        <h1 className='mobile'>
          {this.getHackmitDate()}
          <br />
          {this.getTitle()}
        </h1>

        <TimeMachine currentDate={this.props.currentDate} />

        <Notepad title='Sent codewords' />

        <br style={{clear: 'both'}} />
      </div>
    )
  }
}

export default FuturePane
