import { useState } from "react"
import dynamic from "next/dynamic"
import ListView from "@/components/ListView"
import Sidebar from "@/components/Sidebar"

interface FeatureData {
  id: string
  attributes: Record<string, any>
}

const CampusMap = dynamic(() => import("../components/CampusMap"), { ssr: false })

export default function HomePage() {
  function handleButtonClick(): void {
    alert("Button clicked!")
  }

  const [features, setFeatures] = useState<FeatureData[]>([])
  const [view, setView] = useState<"map" | "list">("map")

  return (
    <div className="flex h-screen">
      <div className="w-72 p-4 border-r border-gray-300">
        <h3 className="text-lg font-semibold mb-4">Control Panel</h3>
        <button
          onClick={() => setView("map")}
          className={`w-full mb-2 px-4 py-2 text-white rounded ${view === "map" ? "bg-blue-600" : "bg-blue-400"}`}
        >
          Map View
        </button>
        <button
          onClick={() => setView("list")}
          className={`w-full px-4 py-2 text-white rounded ${view === "list" ? "bg-blue-600" : "bg-blue-400"}`}
        >
          List View
        </button>
      </div>
      <Sidebar />
      <div className="flex-1">{view === "map" ? <CampusMap setFeatures={setFeatures} /> : <ListView />}</div>
    </div>
  )
}
