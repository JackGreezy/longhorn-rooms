import React, { useEffect, useRef, useState } from "react"
import WebMap from "@arcgis/core/WebMap"
import MapView from "@arcgis/core/views/MapView"
import OAuthInfo from "@arcgis/core/identity/OAuthInfo"
import IdentityManager from "@arcgis/core/identity/IdentityManager"
import FeatureLayer from "@arcgis/core/layers/FeatureLayer"

interface FeatureData {
  id: string
  attributes: Record<string, any>
}

const CampusMap: React.FC = () => {
  const mapDiv = useRef<HTMLDivElement>(null)
  const [features, setFeatures] = useState<FeatureData[]>([])

  useEffect(() => {
    if (typeof window === "undefined") return // Exit if not in the browser

    const initializeMap = async () => {
      try {
        const info = new OAuthInfo({
          appId: process.env.CLIENT_ID || "",
          portalUrl: "https://www.arcgis.com",
          popup: true,
        })
        IdentityManager.registerOAuthInfos([info])

        const webMap = new WebMap({
          portalItem: {
            id: "2ae983502d6840fea528343b628b87a9",
          },
        })

        const view = new MapView({
          container: mapDiv.current as HTMLDivElement,
          map: webMap,
        })

        await view.when()
        console.log("Map and View loaded")

        const fetchedFeatures: FeatureData[] = []

        webMap.allLayers.forEach(async (layer) => {
          if (layer.type === "feature") {
            const featureLayer = layer as FeatureLayer

            const query = featureLayer.createQuery()
            query.returnGeometry = false
            query.outFields = ["*"]

            try {
              const result = await featureLayer.queryFeatures(query)
              console.log(`Features in ${featureLayer.title}:`, result.features)

              result.features.forEach((feature) => {
                fetchedFeatures.push({
                  id: feature.attributes.OBJECTID,
                  attributes: feature.attributes,
                })
              })

              setFeatures((prevFeatures) => [...prevFeatures, ...fetchedFeatures])
            } catch (error) {
              console.error(`Error querying features for ${featureLayer.title}:`, error)
            }
          }
        })
      } catch (error) {
        console.error("Error loading map:", error)
      }
    }

    initializeMap()

    return () => {
      if (mapDiv.current) {
        mapDiv.current.innerHTML = ""
      }
    }
  }, [])

  return (
    <div style={{ display: "flex", height: "100vh", width: "100%" }}>
      <div ref={mapDiv} style={{ flex: 1, height: "100%" }} />
      <div style={{ width: "300px", overflowY: "scroll", padding: "10px", borderLeft: "1px solid #ccc" }}>
        <h3>Feature Layer Data</h3>
        {features.length > 0 ? (
          <ul>
            {features.map((feature) => (
              <li key={feature.id}>
                <strong>ID:</strong> {feature.id}
                <br />
                <strong>Attributes:</strong>
                <ul>
                  {Object.entries(feature.attributes).map(([key, value]) => (
                    <li key={key}>
                      {key}: {value?.toString() || "N/A"}
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        ) : (
          <p>Loading features...</p>
        )}
      </div>
    </div>
  )
}

export default CampusMap
