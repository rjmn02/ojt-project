import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import axios from "axios";

const ProtectedRoute = ({
  children,
  allowedRoles,
}: {
  children: React.ReactNode;
  allowedRoles?: string[];
}) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [unauthorized, setUnauthorized] = useState(false);

  useEffect(() => {
    axios
      .get("/auth/me", { withCredentials: true })
      .then((res) => {
        const user = res.data;
        if (allowedRoles && !allowedRoles.includes(user.type)) {
          setUnauthorized(true);
        } else {
          setUser(user);
        }
      })
      .catch(() => setUnauthorized(true))
      .finally(() => setLoading(false));
  }, [allowedRoles]);

  if (loading) return <div>Loading...</div>;
  if (unauthorized) return <Navigate to="/login" replace />;

  return <>{children}</>;
};

export default ProtectedRoute;
