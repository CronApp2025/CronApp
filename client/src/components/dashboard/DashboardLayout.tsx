
import React from "react";
import { Header } from "./Header";
import { Sidebar } from "./Sidebar";
import { Footer } from "./Footer";
import { MobileNavigation } from "./mobile-navigation";
import { useIsMobile } from "@/hooks/use-mobile";
import { useAuth } from "@/hooks/use-auth";
import { LoadingScreen } from "@/components/ui/loading-screen";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const isMobile = useIsMobile();
  const { isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen message="Cargando dashboard..." />;
  }

  return (
    <div className="min-h-screen bg-white">
      <Header activePath={window.location.pathname} />
      
      <div className="flex flex-1">
        {!isMobile && (
          <div className="w-80 fixed inset-y-0 top-16 bg-white border-r border-neutral-200 overflow-y-auto">
            <Sidebar className="p-6" />
          </div>
        )}
        
        <main className={`flex-1 ${!isMobile ? 'ml-80' : ''} p-6`}>
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
      
      <Footer />
      {isMobile && <MobileNavigation />}
    </div>
  );
}
