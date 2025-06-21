import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const MainPage = () => {
  const navigate = useNavigate()
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    axios.get('/auth/me', { withCredentials: true })
      .then(res => {
        setEmail(res.data.email);
      })
      .catch(err => {
        console.error("Error fetching user info", err);
      });
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <h1>Welcome {email || "Guest"}</h1>
    </div>
  );
};

export default MainPage;
