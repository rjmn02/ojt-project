import { useEffect, useState } from "react";
import axios from "axios";
import type { User } from "@/lib/types";
import { DataTable } from "./data-table";
import { columns } from "./columns";
import UserForm from "@/components/UserForm";

const UsersPage = () => {
  const [users, setUsers] = useState<User[]>([]);

  const fetchUsers = () => {
    axios
      .get("/api/users", {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      })
      .then((res) => {
        setUsers(res.data);
      })
      .catch((error: any) => {
        console.error("Error fetching users", error);
      });
  };

  useEffect(() => {
    document.title = "Users";
    fetchUsers();
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="flex items-center justify-center gap-20 p-6">
        <div>
          <h1 className="text-3xl font-bold text-center mb-3">User Form</h1>
          <UserForm onUserChange={fetchUsers} />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-center mb-3">Users</h1>
          <DataTable columns={columns} data={users} />
        </div>
      </div>
    </div>
  );
};

export default UsersPage;
