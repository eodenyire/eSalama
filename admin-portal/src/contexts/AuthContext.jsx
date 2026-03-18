import React, { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (token && storedUser) {
      setUser(JSON.parse(storedUser))
      authAPI.getCurrentUser()
        .then(res => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
        })
    }
    
    setLoading(false)
  }, [])

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      const { access_token } = response.data
      
      localStorage.setItem('token', access_token)
      
      const userResponse = await authAPI.getCurrentUser()
      const userData = userResponse.data
      
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
