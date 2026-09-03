import Sidebar from "@/components/layout/Sidebar";


export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-50">

      <Sidebar />

      <main className="md:ml-64">
        {children}
      </main>

    </div>
  );
}