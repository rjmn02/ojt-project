import { useEffect, useState } from 'react';

const MainPage = () => {
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token"); // should be "token" if that's what you're storing
    if (!token) return;

    try {
      const payloadBase64 = token.split('.')[1];
      const decodedPayload = JSON.parse(atob(payloadBase64));
      setEmail(decodedPayload.sub); // "sub" is the user's email in your token
    } catch (error) {
      console.error("Invalid token", error);
    }
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <h1>Welcome {email || "Guest"}</h1>
    </div>
  );
};

export default MainPage;
