
import type { User } from "@/lib/types";
import type { ColumnDef } from "@tanstack/react-table"

export const columns: ColumnDef<User>[] = [
  {
    accessorKey: "id",
    header: () => <div className="text-left p-3">ID</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('id')}</div>;
    },
  },
  {
    accessorKey: "firstname",
    header: () => <div className="text-left p-3">Firstname</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('firstname')}</div>;
    },
  },
  {
    accessorKey: "middlename",
    header: () => <div className="text-left p-3">Middlename</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('middlename')}</div>;
    },
  },
  {
    accessorKey: "lastname",
    header: () => <div className="text-left p-3">Lastname</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('lastname')}</div>;
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
    header: () => <div className="text-left p-3">Status</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('status')}</div>;
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
  }
]