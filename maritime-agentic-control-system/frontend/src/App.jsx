import React, { useState } from 'react';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import VesselTracking from './pages/VesselTracking';
import EventMonitor from './pages/EventMonitor';
import RiskAnalysis from './pages/RiskAnalysis';
import RouteRecommendations from './pages/RouteRecommendations';
import Settings from './pages/Settings';
import GovernanceDashboard from './pages/GovernanceDashboard';
import './index.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard activeTab="dashboard" />;
      case 'workflow':
        return <Dashboard activeTab="workflow" />;
      case 'tracking':
        return <VesselTracking />;
      case 'monitor':
        return <EventMonitor />;
      case 'risk':
        return <RiskAnalysis />;
      case 'routes':
        return <RouteRecommendations />;
      case 'governance':
        return <GovernanceDashboard />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard activeTab="dashboard" />;
    }
  };

  return (
    <MainLayout activeTab={activeTab} setActiveTab={setActiveTab}>
      {renderContent()}
    </MainLayout>
  );
}
