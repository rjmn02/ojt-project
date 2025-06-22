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
import { useEffect } from "react";
import { toast } from "sonner";
import { type Car, CarStatus, FuelType, TransmissionType } from "@/lib/types";

interface UserFormProps {
  currentCar?: Car;
}

const formSchema = z.object({
  vin: z.string().min(1, "VIN Number is required"),
  year: z.coerce.number().max(3000),
  make: z.string().min(1, "Make is required"),
  model: z.string().min(1, "Model is required"),
  color: z.string().min(1, "Color is required"),
  mileage: z.coerce.number(),
  price: z.coerce.number(),
  transmission_type: z.enum(["MANUAL", "AUTOMATIC"]),
  fuel_type: z.enum(["PETROL", "DIESEL", "ELECTRIC", "HYBRID"]),
  status: z.enum(["AVAILABLE", "SOLD", "RESERVED"]),
});

const CarsForm: React.FC<UserFormProps> = ({ currentCar }) => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: currentCar
      ? {
          vin: currentCar.vin,
          year: currentCar.year,
          make: currentCar.make,
          model: currentCar.model,
          color: currentCar.color,
          mileage: currentCar.mileage,
          price: currentCar.price,
          transmission_type: currentCar.transmission_type as TransmissionType,
          fuel_type: currentCar.fuel_type as FuelType,
          status: currentCar.status as CarStatus,
        }
      : {
          vin: "",
          year: 1900,
          make: "",
          model: "",
          color: "",
          mileage: 1,
          price: 1,
          transmission_type: TransmissionType.MANUAL,
          fuel_type: FuelType.PETROL,
          status: CarStatus.AVAILABLE,
        },
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    console.log(values);
    console.log(form.formState.errors);

    if (currentCar) {
      axios
        .put(`/api/cars/${currentCar.id}`, values, {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        })
        .then((response) => {
          console.log(response);
          form.reset();
          toast.success("Car details updated, refresh page to see changes");
        })
        .catch((error) => {
          const message = error.response.data.detail || "Unexpected error";
          toast.error(message);
        });
    } else {
      axios
        .post("/api/cars", values, {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        })
        .then((response) => {
          console.log(response);
          form.reset();
          toast.success("Car added, refresh page to see changes");
        })
        .catch((error) => {
          const message = error.response.data.detail || "Unexpected error";
          toast.error(message);
        });
    }
  };

  useEffect(() => {}, []);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="vin"
          render={({ field }) => (
            <FormItem>
              <FormLabel>VIN Number:</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>Input VIN Number</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="year"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Year:</FormLabel>
              <FormControl>
                <Input
                  {...field}
                  type="number"
                  value={field.value ? Number(field.value) : 0}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormDescription>Input the car's model year</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="make"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Make:</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>Input the car's manufacturer</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="model"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Model:</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>Input the car's model</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="color"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Color:</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>Input the car's color</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className="grid grid-cols-2 grid-rows-1 gap-4">
          <FormField
            control={form.control}
            name="mileage"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Mileage (KM):</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="number"
                    value={field.value ? Number(field.value) : 0}
                    onChange={(e) => field.onChange(Number(e.target.value))}
                  />
                </FormControl>
                <FormDescription>
                  Input the car's mileage in Kilometers
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="price"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Price (PHP):</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="number"
                    value={field.value ? Number(field.value) : 0}
                    onChange={(e) => field.onChange(Number(e.target.value))}
                  />
                </FormControl>
                <FormDescription>
                  Input the car's price in Philippine Peso
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-3 grid-rows-1 gap-4">
          <FormField
            control={form.control}
            name="transmission_type"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Transmission Type:</FormLabel>
                <Select
                  onValueChange={(value) =>
                    field.onChange(value ? (value as TransmissionType) : null)
                  }
                  defaultValue={field.value?.toString() || ""}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Transmission" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={"MANUAL"}>MANUAL</SelectItem>
                    <SelectItem value={"AUTOMATIC"}>AUTOMATIC</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="fuel_type"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Fuel Type:</FormLabel>
                <Select
                  onValueChange={(value) =>
                    field.onChange(value ? (value as FuelType) : null)
                  }
                  defaultValue={field.value?.toString() || ""}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Account Type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={"PETROL"}>PETROL</SelectItem>
                    <SelectItem value={"DIESEL"}>DIESEL</SelectItem>
                    <SelectItem value={"ELECTRIC"}>ELECTRIC</SelectItem>
                    <SelectItem value={"HYBRID"}>HYBRID</SelectItem>
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
                <FormLabel>Status:</FormLabel>
                <Select
                  onValueChange={(value) =>
                    field.onChange(value ? (value as CarStatus) : null)
                  }
                  defaultValue={field.value?.toString() || ""}
                  disabled={!currentCar}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select Car Status" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={"AVAILABLE"}>AVAILABLE</SelectItem>
                    <SelectItem value={"SOLD"}>SOLD</SelectItem>
                    <SelectItem value={"RESERVED"}>RESERVED</SelectItem>
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

export default CarsForm;
