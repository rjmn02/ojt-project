import React from "react";

import ReactDOM from "react-dom/client";
import "./index.css";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import Login from "./components/pages/main/Login";
import { ThemeProvider } from "./components/theme-provider";
import Body from "./components/pages/layout/Body";
import ProtectedRoute from "./components/ProtectedRoute";
import MainPage from "./components/pages/main/MainPage";
import Register from "./components/pages/main/Register";
import SystemLogsPage from "./components/pages/main/SystemLogs/SystemLogsPage";
import UsersPage from "./components/pages/main/Users/UsersPage";
import CarsPage from "./components/pages/main/Cars/CarsPage";
import Unauthorized from "./components/pages/main/Unauthorized";
import ProfilePage from "./components/pages/main/ProfilePage";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/unauthorized" element={<Unauthorized />} />
      <Route
        path="/"
        element={
          <ProtectedRoute allowedUsers={["ADMIN", "MANAGER"]}>
            <Body element={<MainPage />} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/profile"
        element={
          <ProtectedRoute allowedUsers={["ADMIN", "MANAGER"]}>
            <Body element={<ProfilePage />} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/cars"
        element={
          <ProtectedRoute allowedUsers={["ADMIN", "MANAGER"]}>
            <Body element={<CarsPage />} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/system-logs"
        element={
          <ProtectedRoute allowedUsers={["ADMIN"]}>
            <Body element={<SystemLogsPage />} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/users"
        element={
          <ProtectedRoute allowedUsers={["ADMIN"]}>
            <Body element={<UsersPage />} />
          </ProtectedRoute>
        }
      />
    </>
  )
);

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
);
