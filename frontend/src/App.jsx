import { useState } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'

export default function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])

  const sendMessage = async () => {
    if (!input) return

    const res = await axios.post('http://localhost:8000/chat', {
      question: input,
    })

    setMessages([
      ...messages,
      { user: input, bot: res.data.response },
    ])

    setInput('')
  }

  return (
    <div style={{ background: '#0b0b0b', color: 'white', height: '100vh', padding: '20px' }}>
      <h1 style={{ textAlign: 'center', fontSize: '28px' }}>
        Westeros Oracle 🐉
      </h1>

      <div style={{ marginTop: '20px' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: '15px' }}>
            <p>👤 {m.user}</p>
            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ color: '#facc15' }}>
              🤖 {m.bot}
            </motion.p>
          </div>
        ))}
      </div>

      <div style={{ position: 'fixed', bottom: '20px', width: '90%', display: 'flex', gap: '10px' }}>
        <input
          style={{ flex: 1, padding: '10px' }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
}