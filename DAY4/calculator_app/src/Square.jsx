import { useState } from 'react'
export default function Square(){
    const[num,setNum]= useState(0) //useState is used for assigning the initial state  
    const[sqr,setsqr]= useState(0)
    return(
        <>
        <p>Number : <input type="number"
                    value={num} onChange={(e) => {setNum(parseInt(e.target.value));}}/></p>
                    <p><button onClick={() => {setsqr(num*num);}}>Calculate Square</button></p>
        
        <p>Square of { num } is { sqr }</p>
        </>

    )
}