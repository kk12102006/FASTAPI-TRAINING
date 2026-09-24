import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'


import About from './About'
import Square from './Square'
import Sumcalc from './Sumclac'


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <p>My Application</p>
    <hr></hr>
    <About/>
    <hr></hr>
    <Square/>
    <hr></hr>
    <Sumcalc/>
    </>
  )
}

export default App
