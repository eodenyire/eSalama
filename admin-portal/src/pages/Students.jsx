import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { studentsAPI } from '../services/api'

export default function Students() {
  const { data: students, isLoading, error } = useQuery({
    queryKey: ['students'],
    queryFn: async () => {
      const response = await studentsAPI.getAll()
      return response.data
    },
  })

  if (isLoading) {
    return <div className="p-8">Loading...</div>
  }

  if (error) {
    return <div className="p-8 text-red-600">Error loading students</div>
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Students</h1>
        <p className="text-gray-600 mt-2">Manage student records</p>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4">Student ID</th>
                <th className="text-left py-3 px-4">Name</th>
                <th className="text-left py-3 px-4">Class</th>
                <th className="text-left py-3 px-4">Device</th>
                <th className="text-left py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {students?.map((student) => (
                <tr key={student.id} className="border-b hover:bg-gray-50">
                  <td className="py-3 px-4">{student.student_id}</td>
                  <td className="py-3 px-4 font-medium">{student.full_name}</td>
                  <td className="py-3 px-4">{student.class_name || 'N/A'}</td>
                  <td className="py-3 px-4">
                    {student.device_id ? (
                      <span className="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">
                        {student.device_type}
                      </span>
                    ) : (
                      <span className="text-sm text-gray-500">No device</span>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    {student.is_active ? (
                      <span className="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">
                        Active
                      </span>
                    ) : (
                      <span className="text-sm bg-gray-100 text-gray-800 px-2 py-1 rounded">
                        Inactive
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {(!students || students.length === 0) && (
            <div className="text-center py-8 text-gray-500">
              No students found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
