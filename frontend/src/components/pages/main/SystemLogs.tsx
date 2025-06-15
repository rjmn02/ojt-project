import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import axios from "axios";
import type { SystemLog } from "@/lib/types";



const SystemLogs = () => {
  const [logs, setLogs] = useState<SystemLog[]>([]);


  const fetchLogs = () => {
   const token = localStorage.getItem("access_token") || "";

    axios
      .get(`${import.meta.env.VITE_API_URL}/api/system-logs`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response: any) => {
        console.log(response);
        setLogs(response.data.data);
      })
      .catch((error: any) => {
        console.error("Error fetching system logs:", error);
      });
  }

  useEffect(() => {
    document.title = "System Logs";
    fetchLogs();
  }, []);

  return (
    <div className="flex flex-col items-center space-y-8 min-h-screen mt-25">
      <h1 className="text-3xl font-bold">System Logs</h1>
      <div>
        <Table className="w-[700px]">
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">ID</TableHead>
              <TableHead className="w-[100px]">User</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Created By</TableHead>
              <TableHead>Created Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {logs.map((log: SystemLog) => (
              <TableRow key={log.id}>
                <TableCell>{log.id}</TableCell>
                <TableCell>
                  {log.user.username}
                  <br />
                  {log.user.email}
                </TableCell>
                <TableCell>{log.description}</TableCell>
                <TableCell>{log.created_by}</TableCell>
                <TableCell>{new Date(log.created_date).toLocaleString()}</TableCell>
                
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default SystemLogs;
