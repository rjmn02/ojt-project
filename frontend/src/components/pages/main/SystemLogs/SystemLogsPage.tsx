import { useEffect, useState } from "react";
import axios from "axios";
import type { SystemLog } from "@/lib/types";
import { DataTable } from "./data-table";
import { columns } from "./columns";

const SystemLogsPage = () => {
  const [logs, setLogs] = useState<SystemLog[]>([]);

  const fetchLogs = () => {
    axios
      .get('/api/system_logs?page=0&page_size=50', {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      })
      .then((res) => {
        setLogs(res.data)
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
      <h1 className="text-3xl font-bold">System Logs (Last 50 logs)</h1>
      <div>
        <DataTable columns={columns} data={logs} />
      </div>
    </div>
  );
};

export default SystemLogsPage;

