import type { AccountType } from "@/lib/types";
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({
  children,
  allowedUsers,
}: {
  children: React.ReactNode;
  allowedUsers: string[];
}) => {
  const [authorized, setAuthorized] = useState<boolean | null>(null); // null = loading

  const navigate = useNavigate()
  useEffect(() => {
    axios
      .get('/auth/me', { withCredentials: true })
      .then((res) => {
        setAuthorized(allowedUsers.includes(res.data.type as AccountType));
      })
      .catch((error) => {
        console.error("Error fetching user type:", error);
        setAuthorized(false);
      });
  }, [allowedUsers]);

  if (authorized === null) {
    return <div>Loading...</div>;
  }

  if (!authorized) {
    navigate('/login')
  }

  return <>{children}</>;
};

export default ProtectedRoute;
