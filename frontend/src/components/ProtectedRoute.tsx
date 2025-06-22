import type { User } from "@/lib/types";
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
  const [user, setUser] = useState<User | null>(null);
  const [authorized, setAuthorized] = useState<boolean | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await axios.get("/auth/me", { withCredentials: true });
        const fetchedUser: User = res.data;
        setUser(fetchedUser);

        if (allowedUsers.includes(fetchedUser.type)) {
          setAuthorized(true);
        } else {
          setAuthorized(false);
        }
      } catch (error) {
        console.error("Error fetching user:", error);
        setUser(null);
        setAuthorized(false);
      }
    };

    fetchUser();
  }, [allowedUsers]);

  useEffect(() => {
    if (authorized === false && user === null) {
      navigate("/login");
    } else if (authorized === false) {
      navigate("/unauthorized");
    }
  }, [authorized, user, navigate]);

  if (authorized === null) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
