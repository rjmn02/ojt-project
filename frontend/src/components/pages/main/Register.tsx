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
import { Button } from "@/components/ui/button";
import axios from "axios";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

enum RegAccountType {
  AGENT = "AGENT",
}


const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),

  firstname: z.string().min(1, "Firstname is required"),
  middlename: z.string(),
  lastname: z.string().min(1, "Lastname is required"),
  contact_num: z.string().min(1, "Contact number is required"),

  type: z.enum(["AGENT", "CLIENT"]),
});

const Register = () => {
  const navigate = useNavigate()

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",

      firstname: "",
      middlename: "",
      lastname: "",
      contact_num: "",

      type: RegAccountType.AGENT,
    },
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    axios
      .post('/auth/register', values, {
        headers: {
          "Content-Type": "application/json"
        },
        withCredentials: true,
      })
      .then((response) => {
        console.log(response);
        form.reset();
        navigate('/')
      })
      .catch((error) => {
        console.error("Error registering:", error);
      });
  };

  useEffect(() => {
    document.title = "Registration Page";
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen">
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
                      // disabled={!!currentUser}
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
                      field.onChange(value ? value : null)
                    }
                    defaultValue={field.value?.toString() || ""}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select Account Type" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value={"AGENT" as RegAccountType.AGENT}>AGENT</SelectItem>
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
    </div>
  );
};

export default Register;
