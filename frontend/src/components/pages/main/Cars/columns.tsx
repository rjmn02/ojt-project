
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import UserForm from "@/components/UserForm";
import type { User } from "@/lib/types";
import type { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"

export const columns: ColumnDef<User>[] = [
  {
    accessorKey: "id",
    header: () => <div className="text-left p-3">ID</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('id')}</div>;
    },
  },
  {
    accessorKey: "email",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Email
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
  },
  {
    id: "fullName",
    header: () => <div className="text-left p-3">Full Name</div>,
    cell: ({ row }) => {
      const { firstname, middlename, lastname } = row.original;
      const fullName = [firstname, middlename, lastname].filter(Boolean).join(" ");
      return <div className="text-left p-3">{fullName}</div>;
    },
  },
  {
    accessorKey: "contact_num",
    header: () => <div className="text-left p-3">Contact Number</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('contact_num')}</div>;
    },
  },
  {
    accessorKey: "type",
    header: () => <div className="text-left p-3">Type</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('type')}</div>;
    },
  },
  {
    accessorKey: "status",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Status
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
  },
  {
    accessorKey: "updated_at",
    header: () => <div className="text-left p-3">Last Updated At</div>,
    cell: ({ row }) => {
      const updated_at = row.getValue("updated_at") as Date;
      const formattedDate = new Date(updated_at).toLocaleString(); // Adjust formatting as needed

      return <div className="text-left p-3">{formattedDate}</div>;
    },
  },
  {
    id: "actions",
    header: () => <div className="text-left p-3">Actions</div>,
    cell: ({ row }) => {
      const user = row.original
 
      return (
        <div className="flex flex-row gap-4">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline">Edit</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogTitle className="text-center">User Edit Form</DialogTitle>
              <UserForm currentUser={user}/>
            </DialogContent>
          </Dialog>
        </div>
        
      )
    },
  },
]