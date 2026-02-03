import React, { useState, useEffect } from 'react'
import { Users, CheckCircle, AlertCircle, Navigation } from 'lucide-react'
import { studentsAPI, attendanceAPI } from '../services/api'
import { useQuery } from '@tanstack/react-query'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalStudents: 0,
    presentToday: 0,
    inTransit: 0,
    alerts: 0,
  })

  const { data: students } = useQuery({
    queryKey: ['students'],
    queryFn: async () => {
      const response = await studentsAPI.getAll()
      return response.data
    },
  })

  const { data: attendance } = useQuery({
    queryKey: ['attendance'],
    queryFn: async () => {
      const today = new Date().toISOString().split('T')[0]
      const response = await attendanceAPI.getRecords({ date: today })
      return response.data
    },
  })

  useEffect(() => {
    if (students && attendance) {
      setStats({
        totalStudents: students.length,
        presentToday: attendance.filter(a => a.type === 'arrival').length,
        inTransit: Math.floor(Math.random() * 10), // Placeholder
        alerts: 0,
      })
    }
  }, [students, attendance])

  const statCards = [
    {
      title: 'Total Students',
      value: stats.totalStudents,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      title: 'Present Today',
      value: stats.presentToday,
      icon: CheckCircle,
      color: 'bg-green-500',
    },
    {
      title: 'In Transit',
      value: stats.inTransit,
      icon: Navigation,
      color: 'bg-yellow-500',
    },
    {
      title: 'Alerts',
      value: stats.alerts,
      icon: AlertCircle,
      color: 'bg-red-500',
    },
  ]

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to eSalama Admin Portal</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat) => (
          <div key={stat.title} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.title}</p>
                <p className="text-3xl font-bold mt-2">{stat.value}</p>
              </div>
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <div className="space-y-4">
          {attendance?.slice(0, 5).map((record, idx) => (
            <div key={idx} className="flex items-center justify-between py-3 border-b last:border-b-0">
              <div>
                <p className="font-medium">Student ID: {record.student_id}</p>
                <p className="text-sm text-gray-600">
                  {record.type === 'arrival' ? 'Arrived at school' : 'Departed from school'}
                </p>
              </div>
              <p className="text-sm text-gray-500">
                {new Date(record.timestamp).toLocaleTimeString()}
              </p>
            </div>
          ))}
          {(!attendance || attendance.length === 0) && (
            <p className="text-gray-500 text-center py-4">No recent activity</p>
          )}
        </div>
      </div>
    </div>
  )
}
