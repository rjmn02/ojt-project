import type { User } from "@/lib/types"
import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import axios from "axios";
import UserForm from "@/components/UserForm";


const Users = () => {
  const [users, setUsers] = useState<User[]>([])

  const fetchUsers = () => {
    const token = localStorage.getItem("access_token") || ""

    axios
      .get(`${import.meta.env.VITE_API_URL}/api/users`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response: any) => {
        const normalizedUsers = response.data.data.map((user: any) => ({
          ...user,
          created_date: new Date(user.created_date),
          updated_date: user.updated_date ? new Date(user.updated_date) : null,
        }))
        setUsers(normalizedUsers)
      })
      .catch((error: any) => {
        console.error("Error fetching users:", error)
      })
  }

  const handleDeleteUser = (userId: number) => {
    const token = localStorage.getItem("access_token") || ""

    axios
    .delete(`${import.meta.env.VITE_API_URL}/api/delete-user/${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
    .then((response: any) => {
      console.log("User deleted successfully:", response.data)
      fetchUsers()
    })
    .catch((error: any) => {
      console.error("Error fetching users:", error)
    })
    
  }

  const handleOpenChange = (open: boolean) => {
    if (!open) {
      fetchUsers()
    }
  }

  useEffect(() => {
    document.title = "Users"
    fetchUsers()
  }, [])

  return (
    <div className="flex flex-col items-center space-y-8 min-h-screen mt-25">
      <div className="flex justify-between w-[800px]">
        <h1 className="text-3xl font-bold">Items</h1>
        <Dialog onOpenChange={handleOpenChange}>
          <DialogTrigger>
             <Button>Create User</Button> 
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create User Form</DialogTitle>
            </DialogHeader>
      
            <UserForm />
          </DialogContent>
        </Dialog>
      </div>
      <div>
        <Table className="w-[700px]">
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">ID</TableHead>
              <TableHead>Full Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Contact Number</TableHead>
              <TableHead>Account Type</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users?.map((user: User) => (
              <TableRow key={user.id}>
                <TableCell>{user.id}</TableCell>
                <TableCell>{user.firstname} {user.middlename} {user.lastname}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.contact_num}</TableCell>
                <TableCell>{user.account_type}</TableCell>
                <TableCell>{user.status}</TableCell>

                <TableCell>
                  <div className="flex space-x-2">
                    <Dialog onOpenChange={handleOpenChange}>
                      <DialogTrigger>
                        <Button variant="outline" size="sm">Edit</Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Edit Item Form</DialogTitle>
                        </DialogHeader>
                        <UserForm currentUser={user} />
                      </DialogContent>
                    </Dialog>
                    <Button variant="destructive" size="sm" onClick={ () => {handleDeleteUser(user.id)} }>Delete</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}

export default Users