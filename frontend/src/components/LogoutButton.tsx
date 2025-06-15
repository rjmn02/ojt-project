import { useNavigate } from 'react-router-dom'
import { Button } from './ui/button'

const LogoutButton = () => {
  const navigate = useNavigate()

  return (
    <Button
      variant="destructive"
      onClick={() => {
        localStorage.removeItem("access_token")
        navigate("/login")
      }}
    >
      Logout
    </Button>
  )
}

export default LogoutButton
