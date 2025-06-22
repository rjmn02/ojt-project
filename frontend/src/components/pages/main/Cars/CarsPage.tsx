import type { Car } from "@/lib/types";
import { useEffect, useState } from "react";
import axios from "axios";

import { DataTable } from "./data-table";
import { columns } from "./columns";
import CarsForm from "@/components/CarsForm";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

const CarsPage = () => {
  const [cars, setCars] = useState<Car[]>([]);

  const fetchCars = () => {
    axios
      .get("/api/cars", {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      })
      .then((res) => {
        setCars(res.data);
      })
      .catch((error: any) => {
        console.error("Error fetching cars:", error);
      });
  };

  const handleOpenChange = (open: boolean) => {
    if (!open) fetchCars();
  };

  useEffect(() => {
    document.title = "Cars";
    fetchCars();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <div className="flex items-center justify-between w-[1000px]">
        <h1 className="text-3xl font-bold">Cars</h1>
        <Dialog onOpenChange={handleOpenChange}>
          <DialogTrigger asChild>
            <Button>Add Car</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="text-center">Add Car Form</DialogTitle>
            </DialogHeader>
            <CarsForm />
          </DialogContent>
        </Dialog>
      </div>
      <DataTable columns={columns} data={cars} />
    </div>
  );
};

export default CarsPage;
