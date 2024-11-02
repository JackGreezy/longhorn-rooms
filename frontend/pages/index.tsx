// pages/index.tsx

import React from 'react';
import dynamic from 'next/dynamic';

// Dynamically import CampusMap with SSR disabled
const CampusMap = dynamic(() => import('../components/CampusMap'), { ssr: false });

const HomePage: React.FC = () => {
  return (
    <div>
      <h1>UT Austin Campus Map</h1>
      <CampusMap />
    </div>
  );
};

export default HomePage;
