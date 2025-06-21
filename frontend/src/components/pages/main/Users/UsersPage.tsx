import { useEffect, useState } from "react";
import axios from "axios";
import type {  User } from "@/lib/types";
import { DataTable } from "./data-table";
import { columns } from "./columns";

const UsersPage = () => {
  const [users, setUsers] = useState<User[]>([]);

  const fetchLogs = () => {
    axios
      .get('/api/users', {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      })
      .then((res) => {
        setUsers(res.data)
      })
      .catch((error: any) => {
        console.error("Error fetching users", error);
      });
      
  }

  useEffect(() => {
    document.title = "System Logs";
    fetchLogs();
  }, []);

  return (
    <div className="flex flex-col items-center space-y-8 min-h-screen mt-25">
      <h1 className="text-3xl font-bold">Users</h1>
      <div>
        <DataTable columns={columns} data={users} />
      </div>
    </div>
  );
};

export default UsersPage;

