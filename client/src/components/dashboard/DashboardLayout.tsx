import { ReactNode } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';
import { useIsMobile } from '@/hooks/use-mobile';
import { useState } from 'react';

interface DashboardLayoutProps {
  children: ReactNode;
  activePath: string;
}

export function DashboardLayout({ children, activePath }: DashboardLayoutProps) {
  const isMobile = useIsMobile();
  const [sidebarOpen, setSidebarOpen] = useState(!isMobile);
  
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };
  
  return (
    <div className="min-h-screen bg-neutral-50 flex flex-col">
      <Header 
        activePath={activePath} 
        toggleSidebar={toggleSidebar} 
        sidebarOpen={sidebarOpen}
      />
      
      <div className="flex flex-1 overflow-hidden">
        <Sidebar 
          className={`
            transition-all duration-300 fixed lg:relative z-10 h-[calc(100vh-64px)] 
            ${sidebarOpen ? 'w-64 translate-x-0' : 'w-0 -translate-x-full lg:w-20 lg:translate-x-0'}
          `}
        />
        
        <main 
          className={`
            flex-1 overflow-auto px-4 pb-4 transition-all duration-300
            ${sidebarOpen ? 'lg:ml-64' : 'lg:ml-20'}
          `}
        >
          {/* Sobra detrás del sidebar en móvil */}
          {sidebarOpen && isMobile && (
            <div 
              className="fixed inset-0 bg-black bg-opacity-50 z-0 lg:hidden"
              onClick={() => setSidebarOpen(false)}
            />
          )}
          
          {/* Contenido principal */}
          <div className="py-6">
            {children}
          </div>
        </main>
      </div>
      
      <Footer />
    </div>
  );
}