import { ReactNode } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';
import { MobileNavigation } from './mobile-navigation';
import { useIsMobile } from '@/hooks/use-mobile';

interface DashboardLayoutProps {
  children: ReactNode;
  activePath?: string;
}

export function DashboardLayout({ children, activePath = '/dashboard' }: DashboardLayoutProps) {
  const isMobile = useIsMobile();

  return (
    <div className="min-h-screen bg-neutral-50">
      <Header activePath={activePath} />

      <div className="flex relative">
        {!isMobile && (
          <Sidebar className="w-64 fixed top-16 bottom-0 left-0 bg-white border-r border-neutral-200" />
        )}

        <main className={`flex-1 ${!isMobile ? 'ml-64' : ''} p-4 lg:p-6`}>
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