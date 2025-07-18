import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "./ui/button";
import axios from "axios";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { useEffect, useState } from "react";
import { AccountStatus, AccountType, type User } from "@/lib/types";
import { toast } from "sonner";

interface UserFormProps {
  currentUser?: User;
  onUserChange?: () => void;
  owner?: boolean
}

const formSchema = z.object({
  firstname: z.string().min(1, "Firstname is required"),
  middlename: z.string(),
  lastname: z.string().min(1, "Lastame is required"),
  email: z.string().email("Invalid email address"),
  contact_num: z.string().min(1, "Contact number is required"),
  password: z.string(),
  type: z.enum(["ADMIN", "MANAGER"]).nullable(),
  status: z.enum(["ACTIVE", "INACTIVE"]).nullable(),
});

const UserForm: React.FC<UserFormProps> = ({ currentUser, onUserChange }) => {
  const [isAccountOwner, setIsAccountOwner] = useState<boolean>();
  
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: currentUser
      ? {
          firstname: currentUser?.firstname || "",
          middlename: currentUser?.middlename || "",
          lastname: currentUser?.lastname || "",
          email: currentUser?.email || "",
          contact_num: currentUser?.contact_num || "",
          password: "",
          type: currentUser.type as AccountType,
          status: currentUser.status as AccountStatus,
        }
      : {
          firstname: "",
          middlename: "",
          lastname: "",
          email: "",
          contact_num: "",
          password: "",
          type: AccountType.MANAGER,
          status: AccountStatus.ACTIVE,
        },
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    console.log(values)
    if (currentUser) {
      axios
        .put(`/api/users/${currentUser.id}`, values, {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        })
        .then((response) => {
          console.log(response);
          form.reset();
          toast.success('User details updated, refresh page to see changes')
        })
        .catch((error) => {
          const message = error.response.data.detail || 'Unexpected error'
          toast.error(message);
        });
    } else {
      // New user - create
      axios
        .post(`/api/users`, values, {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        })
        .then((response) => {
          console.log(response);
          form.reset();
          onUserChange?.()
          toast.success('User added, refresh page to see changes')

        })
        .catch((error) => {
          const message = error.response.data.detail || 'Unexpected error'
          toast.error(message);
        });
    }
  };

  const fetchCurrentUser = () => {
    axios
      .get("/auth/me", { withCredentials: true })
      .then((res) => {
        if(currentUser && res.data.id == currentUser.id)
          setIsAccountOwner(true);
      })
      .catch((error) => {
        console.error("Error fetching user:", error);
      });
  };


  useEffect(() => {
    fetchCurrentUser()
  }, []);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* BASIC INFO FIELD */}
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="firstname"
            render={({ field }) => (
              <FormItem>
                <FormLabel>First Name:</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormDescription>Input First Name</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="middlename"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Middle Name:</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormDescription>Input Middle Name</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="lastname"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Last Name:</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormDescription>Input Last Name</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="contact_num"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Contact Number:</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormDescription>Input User Contact Number</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        {/* CREDENTIALS FIELDS */}
        <div className="grid grid-cols-1 gap-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email:</FormLabel>
                <FormControl>
                  <Input {...field} />
                </FormControl>
                <FormDescription>Input User Email</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input
                    type="password"
                    placeholder="Atleast 6 characters"
                    {...field}
                    disabled={!!currentUser && !isAccountOwner}
                  />
                </FormControl>
                <FormDescription>Input Password</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        {/* ACCOUNT DETAILS FIELDS */}
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="type"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Account Type:</FormLabel>
                <Select
                  onValueChange={(value) =>
                    field.onChange(value ? (value as AccountType) : null)
                  }
                  defaultValue={field.value?.toString() || ""}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Account Type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={"ADMIN"}>ADMIN</SelectItem>
                    <SelectItem value={"MANAGER"}>MANAGER</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="status"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Account Status:</FormLabel>
                <Select
                  onValueChange={(value) =>
                    field.onChange(value ? (value as AccountStatus) : null)
                  }
                  defaultValue={field.value?.toString() || ""}
                  disabled={!currentUser}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Account Type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={"ACTIVE"}>ACTIVE</SelectItem>
                    <SelectItem value={"INACTIVE"}>INACTIVE</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <Button type="submit" className="w-full">
          Submit
        </Button>
      </form>
    </Form>
  );
};

export default UserForm;
