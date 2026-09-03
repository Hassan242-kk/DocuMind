"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, FileText, MessageSquare, Search } from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Documents",
    href: "/documents",
    icon: FileText,
  },
  {
    name: "Search",
    href: "/search",
    icon: Search,
  },
  {
    name: "AI Chat",
    href: "/chat",
    icon: MessageSquare,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-64 bg-blue-700 text-white md:block shadow-lg">
      {/* Brand Header */}
      <div className="flex h-16 items-center px-6 border-b border-blue-600/60">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white">
            DocuMind
          </h1>
          <p className="text-xs text-blue-200">AI Document Assistant</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="space-y-1.5 p-4">
        {navigation.map((item) => {
          const Icon = item.icon;
          const active =
            pathname === item.href || pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors ${
                active
                  ? "bg-blue-800 text-white font-semibold shadow-inner"
                  : "text-blue-100 hover:bg-blue-600/70 hover:text-white"
              }`}
            >
              <Icon className={`h-5 w-5 ${active ? "text-white" : "text-blue-200"}`} />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}