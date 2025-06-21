import { useNavigate } from 'react-router-dom'
import { Button } from './ui/button'
import axios from 'axios'

const LogoutButton = () => {
  const navigate = useNavigate()
  
  const handleLogout = () => {
    axios
      .post('/auth/logout',  {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      })
      .then((response) => {
        console.log(response);
        navigate('/login')
      })
      .catch((error) => {
        console.error("Error creating item:", error);
      });
  }
  return (
    <Button
      variant="destructive"
      onClick={() => {handleLogout()}}
    >
      Logout
    </Button>
  )
}

export default LogoutButton
