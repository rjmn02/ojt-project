export interface Item {
  id: number;
  name: string;
  description: string
  created_by: string;
  updated_by:string;
  created_date: Date;
  updated_date: Date;
}

export interface SystemLog {
  id: number;
  user_id: number;
  action: string;
  timestamp: string;
  updated_at: string;   
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
  AGENT = "AGENT",
  CLIENT = "CLIENT"
}

export enum AccountStatus {
  ACTIVE = "ACTIVE",
  INACTIVE = "INACTIVE"
}
