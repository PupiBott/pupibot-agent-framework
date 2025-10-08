import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const OperationDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [operation, setOperation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOperation = async () => {
      try {
        const response = await fetch(`http://localhost:8080/v1/agent/operations/${id}`, {
          headers: {
            Authorization: 'Bearer static_token',
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch operation details');
        }
        const data = await response.json();
        setOperation(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchOperation();
  }, [id]);

  const handleApprove = async () => {
    try {
      const response = await fetch(`http://localhost:8080/v1/agent/operations/${id}/approve`, {
        method: 'PATCH',
        headers: {
          Authorization: 'Bearer static_token',
        },
      });
      if (!response.ok) {
        throw new Error('Failed to approve operation');
      }
      alert('Operation approved successfully');
      navigate('/');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!operation) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Operation Details</h1>
      <p><strong>Operation ID:</strong> {id}</p>
      <p><strong>Status:</strong> {operation.status}</p>
      <p><strong>Result:</strong> {JSON.stringify(operation.result, null, 2)}</p>
      <p><strong>Logs:</strong></p>
      <pre className="bg-gray-100 p-2 rounded">{operation.logs.join('\n')}</pre>

      {operation.status === 'awaiting_confirmation' && (
        <button
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700 mt-4"
          onClick={handleApprove}
        >
          Aprobar
        </button>
      )}

      <button
        className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700 mt-4 ml-4"
        onClick={() => navigate('/')}
      >
        Volver
      </button>
    </div>
  );
};

export default OperationDetail;