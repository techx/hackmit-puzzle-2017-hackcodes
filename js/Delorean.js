import React from 'react'
import FuturePane from './FuturePane'
import PresentPane from './PresentPane'

class Delorean extends React.Component {
  render () {
    return (
      <div className="container">
        <FuturePane />
        <PresentPane />
      </div>
    )
  }
}

export default Delorean
