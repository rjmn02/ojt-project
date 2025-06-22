
const Unauthorized = () => {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-red-600">401</h1>
        <p className="text-xl mt-4 text-gray-700">Unauthorized Access</p>
        <p className="text-md mt-2 text-gray-500">You do not have permission to view this page.</p>
        <a
          href="/"
          className="inline-block mt-6 px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition"
        >
          Go Home
        </a>
      </div>
    </div>
  );
};

export default Unauthorized;
