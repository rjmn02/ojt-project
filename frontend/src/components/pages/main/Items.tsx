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
import ItemForm from "@/components/ItemForm";
import axios from "axios";
import type { Item } from "@/lib/types";


const Items = () => {

  const [items, setItems] = useState<Item[]>();

  const fetchItems = () => {

    const token = localStorage.getItem("access_token") || "";

    axios
      .get(`${import.meta.env.VITE_API_URL}/api/items`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response: any) => {
        const normalizedItems = response.data.data.map((item: any) => ({
          ...item,
          created_date: new Date(item.created_date),
          updated_date: item.updated_date ? new Date(item.updated_date) : null,
        }));
        setItems(normalizedItems);
      })
      .catch((error: any) => {
        console.error("Error fetching system logs:", error);
      });
  }

  const handleDeleteItem = (itemId: number) => {
    const token = localStorage.getItem("access_token") || "";
    axios
      .delete(`${import.meta.env.VITE_API_URL}/api/delete-item/${itemId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response: any) => {
        console.log("Item deleted successfully:", response.data);
        fetchItems();
      })
      .catch((error: any) => {
        console.error("Error deleting item:", error);
      });
  }
  const handleOpenChange = async (open: boolean) => {
    if (!open) {
      fetchItems();
    }
  };


  useEffect(() => {
    document.title = 'Items'
    fetchItems();
  },[])


   return (
    <div className="flex flex-col items-center space-y-8 min-h-screen mt-25">
      <div className="flex justify-between w-[800px]">
        <h1 className="text-3xl font-bold">Users</h1>
        <Dialog onOpenChange={handleOpenChange}>
          <DialogTrigger>
             <Button>Create Item</Button> 
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create Item Form</DialogTitle>
            </DialogHeader>
      
            <ItemForm />
          </DialogContent>
        </Dialog>
      </div>
      <div>
        <Table className="w-[700px]">
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Created By</TableHead>
              <TableHead>Updated By</TableHead>
              <TableHead>Created Date</TableHead>
              <TableHead>Updated Date</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items?.map((item: Item) => (
              <TableRow key={item.id}>
                <TableCell>{item.id}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.description}</TableCell>
                <TableCell>{item.created_by}</TableCell>
                <TableCell>{item.updated_by}</TableCell>
                <TableCell>{item.created_date ? item.created_date.toLocaleString() : 'N/A'}</TableCell>

                <TableCell>{item.updated_date ? item.updated_date.toLocaleString() : 'N/A'}</TableCell>

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
                        <ItemForm currentItem={item}/>
                      </DialogContent>
                    </Dialog>
                    <Button variant="destructive" size="sm" onClick={() => {handleDeleteItem(item.id)}}>Delete</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

export default Items