import React from 'react'

export default function MapView() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Map View</h1>
        <p className="text-gray-600 mt-2">Real-time student location tracking</p>
      </div>

      <div className="card">
        <div className="h-96 flex items-center justify-center bg-gray-100 rounded-lg">
          <div className="text-center text-gray-500">
            <p className="text-lg mb-2">Map View</p>
            <p className="text-sm">Map integration with Leaflet coming soon</p>
          </div>
        </div>
      </div>
    </div>
  )
}
