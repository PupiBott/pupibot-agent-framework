import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { useNavigate } from 'react-router-dom'

function App() {
  const [count, setCount] = useState(0)
  const [operations, setOperations] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchOperations = async () => {
      try {
        const response = await fetch('http://localhost:8080/v1/agent/operations', {
          headers: {
            Authorization: 'Bearer static_token',
          },
        })
        if (!response.ok) {
          throw new Error('Failed to fetch operations')
        }
        const data = await response.json()
        setOperations(data)
      } catch (error) {
        console.error('Error fetching operations:', error)
      }
    }

    fetchOperations()
  }, [])

  const handleViewDetails = (operationId) => {
    navigate(`/operation/${operationId}`)
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Operations</h1>
        <table className="table-auto w-full border-collapse border border-gray-300">
          <thead>
            <tr>
              <th className="border border-gray-300 px-4 py-2">Operation ID</th>
              <th className="border border-gray-300 px-4 py-2">Status</th>
              <th className="border border-gray-300 px-4 py-2">Started At</th>
              <th className="border border-gray-300 px-4 py-2">Finished At</th>
              <th className="border border-gray-300 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {operations.map((operation) => (
              <tr key={operation.operation_id}>
                <td className="border border-gray-300 px-4 py-2">{operation.operation_id}</td>
                <td className="border border-gray-300 px-4 py-2">{operation.status}</td>
                <td className="border border-gray-300 px-4 py-2">{operation.started_at || 'N/A'}</td>
                <td className="border border-gray-300 px-4 py-2">{operation.finished_at || 'N/A'}</td>
                <td className="border border-gray-300 px-4 py-2">
                  <button
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
                    onClick={() => handleViewDetails(operation.operation_id)}
                  >
                    Ver detalles
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

export default App
