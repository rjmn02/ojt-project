
import type { SystemLog } from "@/lib/types"
import type { ColumnDef } from "@tanstack/react-table"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.

export const columns: ColumnDef<SystemLog>[] = [
  {
    accessorKey: "id",
    header: () => <div className="text-left p-3">ID</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('id')}</div>;
    },
  },
  {
    accessorKey: "action",
    header: () => <div className="text-left p-3">Action</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('action')}</div>;
    },
  },
  {
    accessorKey: "timestamp",
    header: () => <div className="text-left p-3">Timestamp</div>,
    cell: ({ row }) => {
      const timestamp = row.getValue("timestamp") as Date;
      const formattedTimestamp = new Date(timestamp).toLocaleString(); // Adjust formatting as needed

      return <div className="text-left p-3">{formattedTimestamp}</div>;
    },
  }

]