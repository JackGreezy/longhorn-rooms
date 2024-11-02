import React, { useEffect, useRef } from 'react';
import WebMap from '@arcgis/core/WebMap';
import MapView from '@arcgis/core/views/MapView';
import OAuthInfo from '@arcgis/core/identity/OAuthInfo';
import IdentityManager from '@arcgis/core/identity/IdentityManager';

const CampusMap: React.FC = () => {
  const mapDiv = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window === 'undefined') return; // Exit if not in the browser

    const initializeMap = async () => {
      try {
        const info = new OAuthInfo({
          appId: process.env.CLIENT_ID || '',
          portalUrl: 'https://www.arcgis.com',
          popup: true,
        });
        IdentityManager.registerOAuthInfos([info]);

        const webMap = new WebMap({
          portalItem: {
            id: '697c20f192481d3a13965918a9b82fb',
          },
        });

        const view = new MapView({
          container: mapDiv.current as HTMLDivElement,
          map: webMap,
        });

        await view.when();
        console.log('Map and View loaded');
      } catch (error) {
        console.error('Error loading map:', error);
      }
    };

    initializeMap();

    return () => {
      if (mapDiv.current) {
        mapDiv.current.innerHTML = '';
      }
    };
  }, []);

  return <div ref={mapDiv} style={{ height: '100vh', width: '100%' }} />;
};

export default CampusMap;
