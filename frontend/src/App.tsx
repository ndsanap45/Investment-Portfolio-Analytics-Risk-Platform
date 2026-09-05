import { useEffect, useState } from 'react'

function App() {
  const [status, setStatus] = useState('Checking backend...')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((response) => response.json())
      .then((data) => {
        setStatus(`${data.status} — ${data.service}`)
      })
      .catch(() => {
        setStatus('Backend connection failed')
      })
  }, [])

  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>Investment Portfolio Analytics & Risk Platform</h1>
      <h3 style={{ textAlign: 'center' }}>Coming Soon</h3>
      {/* <p style={{ textAlign: 'center' }}>Backend Status: {status}</p> */}
    </div>
  )
}

export default App