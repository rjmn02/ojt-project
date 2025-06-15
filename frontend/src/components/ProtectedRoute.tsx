// src/components/ProtectedRoute.tsx


import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem("access_token");
  
  try {
    const payload = JSON.parse(atob(token?.split('.')[1] || ''));
    const isExpired = payload.exp && payload.exp * 1000 < Date.now();
    if (isExpired) throw new Error("Token expired");

  } catch {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
