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
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "./ui/button";
import axios from "axios";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { useEffect } from 'react';
import { AccountStatus, AccountType, type User } from "@/lib/types";


interface UserFormProps {
  currentUser?: User,
}

const formSchema = z.object({
  firstname: z.string().min(1, "Name is required"),
  middlename: z.string().min(1, "Name is required"),
  lastname: z.string().min(1, "Name is required"),
  email: z.string().email("Invalid email address"),
  contact_num: z.string().min(1, "Contact number is required"),
  password: z.string(),
  account_type:  z.enum([
    "SUPER_ADMIN",
  ]).nullable(),
  status:  z.enum([
    "ACTIVE",
    "INACTIVE",
  ]).nullable(),
});

const UserForm: React.FC<UserFormProps> = ({currentUser}) => {

   const form = useForm<z.infer<typeof formSchema>>({
      resolver: zodResolver(formSchema),
      defaultValues: currentUser ? {
        firstname: currentUser?.firstname || "",
        middlename: currentUser?.middlename || "",
        lastname: currentUser?.lastname || "",
        email: currentUser?.email || "",
        contact_num: currentUser?.contact_num || "",
        password: "",
        account_type: currentUser.account_type as AccountType, 
        status: currentUser.status as AccountStatus, 
      } : {
        firstname: "",
        middlename: "",
        lastname: "",
        email: "",
        contact_num: "",
        password: "",
        account_type: AccountType.SUPER_ADMIN,
        status: AccountStatus.ACTIVE,
      }
    })

    

    const onSubmit = (values: z.infer<typeof formSchema>) => {
      const token = localStorage.getItem("access_token") || "";

      if (currentUser) {
        axios
          .put(`${import.meta.env.VITE_API_URL}/api/update-user/${currentUser.id}`, values, {
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          })
          .then((response) => {
            console.log(response);
            form.reset();
          })
          .catch((error) => {
            console.error("Error updating user:", error);
          });
      } else {
        axios
          .post(`${import.meta.env.VITE_API_URL}/api/create-user`, values, {
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          })
          .then((response) => {
            console.log(response);
            form.reset();
          })
          .catch((error) => {
            console.error("Error updating user:", error);
          });
      }
    }

    useEffect(() => {
    }, [])
  
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
                <FormDescription>
                  Input First Name
                </FormDescription>
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
                <FormDescription>
                  Input Middle Name
                </FormDescription>
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
                <FormDescription>
                  Input Last Name
                </FormDescription>
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
                <FormDescription>
                  Input User Contact Number
                </FormDescription>
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
              <FormDescription>
                Input User Email
              </FormDescription>
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
                <Input type="password" placeholder="Atleast 6 characters" {...field} disabled={!!currentUser} />
              </FormControl>
              <FormDescription>
                Input Password
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        </div>
        {/* ACCOUNT DETAILS FIELDS */}
        <div className="grid grid-cols-2 gap-4">
        <FormField
          control={form.control}
          name="account_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Account Type:</FormLabel>
              <Select
                onValueChange={(value) =>
                  field.onChange(value ? value as AccountType : null)
                }
                defaultValue={field.value?.toString() || ""}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select Account Type" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value={"SUPER_ADMIN"}>
                    SUPER_ADMIN
                  </SelectItem>
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
                  field.onChange(value ? value as AccountStatus : null)
                }
                defaultValue={field.value?.toString() || ""}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select Account Type" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value={"ACTIVE"}>
                    ACTIVE
                  </SelectItem>
                   <SelectItem value={"INACTIVE"}>
                    INACTIVE
                  </SelectItem>
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
  )
}

export default UserForm