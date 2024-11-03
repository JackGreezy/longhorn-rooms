import { useEffect, useRef } from "react"
import WebMap from "@arcgis/core/WebMap"
import MapView from "@arcgis/core/views/MapView"
import OAuthInfo from "@arcgis/core/identity/OAuthInfo"
import IdentityManager from "@arcgis/core/identity/IdentityManager"
import FeatureLayer from "@arcgis/core/layers/FeatureLayer"
import { Room } from "@/types/Room"

interface CampusMapProps {
  setRooms: React.Dispatch<React.SetStateAction<Room[]>>
}

export default function CampusMap({ setRooms }: CampusMapProps) {
  const mapDiv = useRef<HTMLDivElement>(null)

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
            id: "c203b2f9de2e44218b84e16eefe40949",
          },
        })

        const view = new MapView({
          container: mapDiv.current as HTMLDivElement,
          map: webMap,
        })

        await view.when()
        console.log("Map and View loaded")

        const fetchedFeatures: Room[] = []

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

              setRooms((prevFeatures) => [...prevFeatures, ...fetchedFeatures])
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
  }, [setRooms]) // eslint-disable-line react-hooks/exhaustive-deps

  return <div ref={mapDiv} style={{ height: "100vh", width: "100%" }} />
}
