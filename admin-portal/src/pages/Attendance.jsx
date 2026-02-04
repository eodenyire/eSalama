import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { attendanceAPI } from '../services/api'
import { format } from 'date-fns'

export default function Attendance() {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0])

  const { data: attendance, isLoading } = useQuery({
    queryKey: ['attendance', selectedDate],
    queryFn: async () => {
      const response = await attendanceAPI.getRecords({ date: selectedDate })
      return response.data
    },
  })

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Attendance</h1>
        <p className="text-gray-600 mt-2">Track student attendance records</p>
      </div>

      <div className="mb-6">
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="input max-w-xs"
        />
      </div>

      <div className="card">
        {isLoading ? (
          <p className="text-center py-8">Loading...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">Student ID</th>
                  <th className="text-left py-3 px-4">Type</th>
                  <th className="text-left py-3 px-4">Time</th>
                  <th className="text-left py-3 px-4">Location</th>
                </tr>
              </thead>
              <tbody>
                {attendance?.map((record) => (
                  <tr key={record.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4">{record.student_id}</td>
                    <td className="py-3 px-4">
                      <span
                        className={`text-sm px-2 py-1 rounded ${
                          record.type === 'arrival'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {record.type}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      {new Date(record.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600">
                      {record.latitude && record.longitude
                        ? `${record.latitude.toFixed(4)}, ${record.longitude.toFixed(4)}`
                        : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(!attendance || attendance.length === 0) && (
              <div className="text-center py-8 text-gray-500">
                No attendance records for this date
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
