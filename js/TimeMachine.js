import React from 'react'

class TimeMachine extends React.Component {
  render () {
    return (
      <div className='time-machine'>
        <textarea id='codeword'></textarea>

        <a id='send-button' className='button'> Send message </a>
      </div>
    )
  }
}

export default TimeMachine
