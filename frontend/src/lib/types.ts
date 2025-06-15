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
  description: string;
  user_id: number;
  created_by: string;
  created_date: string;

  user: {
    id: number;
    username: string;
    email: string;
    logs: any[];
  };
}


export interface User {
  id: number;
  firstname: string;
  middlename: string;
  lastname: string;
  email: string;
  password: string;
  contact_num: string;
  account_type: string;
  status: string;
  created_by: string;
  updated_by:string;
  created_date: Date;
  updated_date: Date;
}

export enum AccountType {
  SUPER_ADMIN = "SUPER_ADMIN",
}

export enum AccountStatus {
  ACTIVE = "ACTIVE",
  INACTIVE = "INACTIVE",
}
