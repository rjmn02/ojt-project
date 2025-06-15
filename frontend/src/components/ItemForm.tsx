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
import type { Item } from "@/lib/types";


const formSchema = z.object({
  name: z.string().min(1, "Name is required"),
  description: z.string().min(1, "Description is required"),
});

interface ItemFormProps {
  currentItem?: Item;
}
const ItemForm: React.FC<ItemFormProps> = ({currentItem}) => {

  const form = useForm<z.infer<typeof formSchema>>({
      resolver: zodResolver(formSchema),
      defaultValues: currentItem ? {
        name: currentItem?.name || "",
        description: currentItem?.description || "",
      } : {
        name: "",
        description:  "",
      }
    })

  const onSubmit = async(values: z.infer<typeof formSchema>) => {
    const token = localStorage.getItem("access_token") || "";

    if(currentItem) {

      axios
      .put(`${import.meta.env.VITE_API_URL}/api/update-item/${currentItem.id}`, values, {
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
        console.error("Error creating item:", error);
      });

    } else {

      axios
      .post(`${import.meta.env.VITE_API_URL}/api/create-item`, values, {
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
        console.error("Error creating item:", error);
      });
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name:</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>
                Input the name of the item
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description: </FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>
                Input the description of the item
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Submit
        </Button>
      </form>
    </Form>
  )
}

export default ItemForm