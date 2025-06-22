import LogoutButton from "@/components/LogoutButton";
import { AccountType } from "@/lib/types";
import axios from "axios";
import { useEffect, useState } from "react";

const Header = () => {
  const [accountType, setAccountType] = useState<AccountType>();

  const fetchUser = () => {
    axios
      .get('/auth/me', { withCredentials: true })
      .then((res) => {
        setAccountType(res.data.type);
      })
      .catch((error) => {
        console.error("Error fetching user:", error);
      });
  }

  useEffect(() => {
    fetchUser()
  }, [])
  
  return (
    <header className="bg-secondary p-4 sticky top-0 z-50">
      <nav>
        <ul className="flex justify-center space-x-8">
          <li>
            <a href="/profile" className="hover:underline">
              Profile
            </a>
          </li>
          {           
            (accountType == AccountType.ADMIN) 
            ? 
            <li>
              <a href="/system-logs" className="hover:underline">
                System Logs
              </a>
            </li>
            :
            <li>
            </li>
          }
          {           
            (accountType == AccountType.ADMIN) 
            ? 
            <li>
              <a href="/users" className="hover:underline">
                Users
              </a>
            </li>
            :
            <li>
            </li>
          }
          <li>
            <a href="/cars" className="hover:underline">
              Cars
            </a>
          </li>
          <li>
            <LogoutButton />
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
