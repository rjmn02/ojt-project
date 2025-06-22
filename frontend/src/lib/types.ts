export interface SystemLog {
  id: number;
  user_id: number;
  action: string;
  timestamp: Date;
  updated_at: Date;   
} 

export interface Car {
  id: number;
  vin: string;
  year: number;
  make: string;
  model: string;
  color: string;
  mileage: number;
  price: number;
  transmission_type: TransmissionType;
  fuel_type: FuelType;
  status: CarStatus;
  created_at: Date; // ISO format Datedate-time string
  updated_at: Date;
  created_by: string;
  updated_by: string;
}


export interface User {
  id: number;
  firstname: string;
  middlename: string;
  lastname: string;
  email: string;
  password: string;
  contact_num: string;
  type: string;
  status: string;
  created_by: string;
  updated_by: string;
  created_at: Date;
  updated_at: Date;
}


export enum TransmissionType {
  MANUAL = "MANUAL",
  AUTOMATIC = "AUTOMATIC"
}

export enum FuelType {
  PETROL = "PETROL",
  DIESEL = "DIESEL",
  ELECTRIC = "ELECTRIC",
  HYBRID = "HYBRID"
}

export enum CarStatus {
  AVAILABLE = "AVAILABLE",
  SOLD = "SOLD",
  RESERVED = "RESERVED"
}

export enum AccountType {
  ADMIN = "ADMIN",
  MANAGER = "MANAGER",
}

export enum AccountStatus {
  ACTIVE = "ACTIVE",
  INACTIVE = "INACTIVE"
}
