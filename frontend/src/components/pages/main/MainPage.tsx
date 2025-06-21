
import axios from 'axios';
import { useEffect, useState } from 'react';

const MainPage = () => {
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get('/auth/me', { withCredentials: true })
      .then((res) => {
        setEmail(res.data.email);
      })
      .catch((error) => {
        console.error("Error fetching user email:", error);
      });
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <h1>Welcome {email || "Guest"}</h1>
    </div>
  );
};

export default MainPage;
