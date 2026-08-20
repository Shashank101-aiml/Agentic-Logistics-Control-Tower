import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import AlertBanner from '../components/AlertBanner';
import { EventProvider, useEventContext } from '../context/EventContext';
import { RiskProvider } from '../context/RiskContext';

const MainContentWrapper = ({ activeTab, setActiveTab, children }) => {
  const { activeAlert, dismissAlert } = useEventContext();

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} systemStatus="OPERATIONAL" />
      <div className="layout-body">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="main-content">
          <AlertBanner 
            alert={activeAlert} 
            onDismiss={dismissAlert} 
            onAction={() => setActiveTab('routes')}
          />
          {children}
        </main>
      </div>
    </div>
  );
};

export default function MainLayout({ activeTab, setActiveTab, children }) {
  return (
    <EventProvider>
      <RiskProvider>
        <MainContentWrapper activeTab={activeTab} setActiveTab={setActiveTab}>
          {children}
        </MainContentWrapper>
      </RiskProvider>
    </EventProvider>
  );
}
