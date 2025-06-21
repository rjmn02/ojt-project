import Footer from "./Footer.tsx";
import Header from "./Header.tsx";
import { Toaster } from "sonner"


const Body = ({ element }: { element: React.ReactNode }) => {
    return (
        <div className="d-flex flex-column min-vh-100">
            <Header />
            <main className="flex-grow-1">
                {element}
            </main>
            <Footer />
            <Toaster /> {/* This ensures it mounts on all protected pages */}
        </div>
    )
}

export default Body;
