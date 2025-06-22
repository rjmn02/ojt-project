
import CarsForm from "@/components/CarsForm";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import UserForm from "@/components/UserForm";
import type { Car } from "@/lib/types";
import type { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"

export const columns: ColumnDef<Car>[] = [
  {
    accessorKey: "id",
    header: () => <div className="text-left p-3">ID</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('id')}</div>;
    },
  },
  {
    accessorKey: "price",
    header: ({column}) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Price (PHP)
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => {
      const value = row.getValue('price');
      const formatted = Number(value).toLocaleString('en-PH', {
        style: 'currency',
        currency: 'PHP',
      });
      return <div className="text-left p-3">{formatted}</div>;
    },
  },
  {
    accessorKey: "vin",
    header: () => <div className="text-left p-3">VIN Number</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('vin')}</div>;
    },
  },
  {
    accessorKey: "year",
    header: ({column}) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Year
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('year')}</div>;
    },
  },
  {
    accessorKey: "make",
    header: () => <div className="text-left p-3">Make</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('make')}</div>;
    },
  },
  {
    accessorKey: "model",
    header: () => <div className="text-left p-3">Model</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('model')}</div>;
    },
  },
  {
    accessorKey: "color",
    header: () => <div className="text-left p-3">Color</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('color')}</div>;
    },
  },
  {
    accessorKey: "mileage",
    header: ({column}) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Mileage (KM)
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => {
      const value = row.getValue('mileage');
      const formatted = Number(value).toLocaleString('en-US');
      return <div className="text-left p-3">{formatted}</div>;
    },
  },
  {
    accessorKey: "transmission_type",
    header: () => <div className="text-left p-3">Transmission</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('transmission_type')}</div>;
    },
  },
  {
    accessorKey: "fuel_type",
    header: () => <div className="text-left p-3">Fuel</div>,
    cell: ({ row }) => {
      return <div className="text-left p-3">{row.getValue('fuel_type')}</div>;
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
    id: "actions",
    header: () => <div className="text-left p-3">Actions</div>,
    cell: ({ row }) => {
      const car = row.original
 
      return (
        <div className="flex flex-row gap-4">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline">Edit</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogTitle className="text-center">Car Edit Form</DialogTitle>
              <CarsForm currentCar={car}/>
            </DialogContent>
          </Dialog>
        </div>
        
      )
    },
  },
]