import React from 'react'

import ReactDOM from 'react-dom/client'
import './index.css'
import {createBrowserRouter, createRoutesFromElements, Route, RouterProvider} from "react-router-dom";
import Login from './components/pages/main/Login';
import { ThemeProvider } from './components/theme-provider';
import Body from './components/pages/layout/Body';
import Items from './components/pages/main/Items';
import ProtectedRoute from './components/ProtectedRoute';
import MainPage from './components/pages/main/MainPage';
import SystemLogs from './components/pages/main/SystemLogs';
import Users from './components/pages/main/Users';


const router = createBrowserRouter(
    createRoutesFromElements(
        <>
            <Route path='/login' element={
                <Login/>
            }/>
            
            <Route path='/' element={
              <ProtectedRoute>
                  <Body element={<MainPage />} />
              </ProtectedRoute>
              } />
            <Route path='/items' element={
              <ProtectedRoute>
                  <Body element={<Items />} />
              </ProtectedRoute>
              } />
            <Route path='/system-logs' element={
              <ProtectedRoute>
                  <Body element={<SystemLogs />} />
              </ProtectedRoute>
              } />
            <Route path='/users' element={
              <ProtectedRoute>
                  <Body element={<Users />} />
              </ProtectedRoute>
              } />
      </>
    )
);


const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
    <React.StrictMode>
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <RouterProvider router={router} />
        </ThemeProvider>
    </React.StrictMode>
)
