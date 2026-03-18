/**
 * eSalama Parent App - Main Entry Point
 */
import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import LoginScreen from './src/screens/LoginScreen';
import HomeScreen from './src/screens/HomeScreen';
import TrackingScreen from './src/screens/TrackingScreen';
import ProfileScreen from './src/screens/ProfileScreen';
import AuthService from './src/services/auth.service';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const MainTabs = () => (
  <Tab.Navigator screenOptions={{ headerShown: false, tabBarActiveTintColor: '#2196F3' }}>
    <Tab.Screen name="Home" component={HomeScreen} options={{ tabBarLabel: 'Notifications' }} />
    <Tab.Screen name="Tracking" component={TrackingScreen} options={{ tabBarLabel: 'Track' }} />
    <Tab.Screen name="Profile" component={ProfileScreen} options={{ tabBarLabel: 'Profile' }} />
  </Tab.Navigator>
);

const App = () => {
  useEffect(() => {
    AuthService.initialize();
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Main" component={MainTabs} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
