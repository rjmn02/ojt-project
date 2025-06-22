import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import UserForm from "@/components/UserForm";
import type { User } from "@/lib/types";
import axios from "axios";
import { useEffect, useState } from "react";

const ProfilePage = () => {
  const [user, setUser] = useState<User | null>(null);

  const fetchUser = () => {
    axios
      .get("/auth/me", { withCredentials: true })
      .then((res) => {
        setUser(res.data);
      })
      .catch((error) => {
        console.error("Error fetching user:", error);
        setUser(null);
      });
  };

  const handleOpenChange = (open: boolean) => {
    if(!open){
      fetchUser()
    }
  }

  useEffect(() => {
    fetchUser();
  }, []);

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-xl">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-5xl font-bold">Profile</h1>
      <div className=" p-8 w-full max-w-md space-y-4">
        <div>
          <h3 className="text-lg font-semibold">Full Name</h3>
          <p>{user.firstname} {user.middlename} {user.lastname}</p>
        </div>
        <div>
          <h3 className="text-lg font-semibold">Email</h3>
          <p>{user.email}</p>
        </div>
         <div>
          <h3 className="text-lg font-semibold">Contact Number</h3>
          <p>{user.contact_num}</p>
        </div>
        <div>
          <h3 className="text-lg font-semibold">Account Type</h3>
          <p>{user.type}</p>
        </div>
        <div>
          <h3 className="text-lg font-semibold">Created At</h3>
          <p>{new Date(user.created_at).toLocaleString()}</p>
        </div>
        <Dialog onOpenChange={handleOpenChange}>
          <DialogTrigger asChild>
            <Button>Edit User Details</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="text-center">Edit User Details</DialogTitle>
            </DialogHeader>
            <UserForm currentUser={user}/>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default ProfilePage;
