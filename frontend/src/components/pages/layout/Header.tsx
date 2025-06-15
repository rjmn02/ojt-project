import LogoutButton from "@/components/LogoutButton";

const Header = () => {
  return (
    <header className="bg-secondary p-4 sticky top-0 z-50">
      <nav>
        <ul className="flex justify-center space-x-8">
          
          <li>
            <a href="/system-logs" className="hover:underline">
              System Logs
            </a>
          </li>
          <li>
            <a href="/items" className="hover:underline">
              Items
            </a>
          </li>
          <li>
            <a href="/users" className="hover:underline">
              Users
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
