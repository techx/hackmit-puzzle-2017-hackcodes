import React from 'react'

class Notepad extends React.Component {
  render () {
    return (
      <div className='notepad display-linebreak'>
        {this.props.title}
        <br />
        <br />
        {this.props.content}
      </div>
    )
  }
}

export default Notepad
